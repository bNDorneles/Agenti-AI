import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from edgecloud_simulator.scenarios import build_demo_scenario
from edgecloud_simulator.simulator import run_simulation
from edgecloud_simulator.strategies import BaselineStrategy, SmartStrategy


def print_result(result):
    print(f"\nStrategy: {result.strategy_name}")
    print("-" * 72)
    print(f"{'Task':<26} {'Node':<16} {'Status':<12} {'Reason'}")
    print("-" * 72)
    for allocation in result.allocations:
        node_name = allocation.node.name if allocation.node else "-"
        status = "allocated" if allocation.node else "rejected"
        print(f"{allocation.task.name:<26} {node_name:<16} {status:<12} {allocation.reason}")

    print("-" * 72)
    print(f"Allocated tasks : {result.allocated_count}")
    print(f"Rejected tasks  : {result.rejected_count}")
    print(f"Average latency : {result.average_latency_ms} ms")
    print(f"Total cost      : {result.total_cost}")
    print(f"Total energy    : {result.total_energy}")


def print_comparison(baseline, smart):
    print("\nComparison summary")
    print("=" * 72)
    print(f"{'Metric':<20} {'Baseline':<15} {'Smart':<15}")
    print("-" * 72)
    rows = [
        ("Allocated", baseline.allocated_count, smart.allocated_count),
        ("Rejected", baseline.rejected_count, smart.rejected_count),
        ("Avg latency", f"{baseline.average_latency_ms} ms", f"{smart.average_latency_ms} ms"),
        ("Total cost", baseline.total_cost, smart.total_cost),
        ("Total energy", baseline.total_energy, smart.total_energy),
    ]
    for metric, baseline_value, smart_value in rows:
        print(f"{metric:<20} {str(baseline_value):<15} {str(smart_value):<15}")

    print("\nInterpretation")
    print("-" * 72)
    print(
        "The baseline strategy is easy to understand, but it depends on node order. "
        "The smart strategy evaluates feasible nodes using latency, resource pressure, "
        "cost, and energy, which makes the allocation decision more explicit and easier "
        "to analyze."
    )


def main():
    tasks, nodes = build_demo_scenario()
    baseline = run_simulation(tasks, nodes, BaselineStrategy())
    smart = run_simulation(tasks, nodes, SmartStrategy())

    print("Mini-Simulator: Edge-Cloud Task Allocation")
    print("=" * 72)
    print_result(baseline)
    print_result(smart)
    print_comparison(baseline, smart)


if __name__ == "__main__":
    main()
