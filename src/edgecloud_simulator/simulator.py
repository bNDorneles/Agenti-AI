from __future__ import annotations

from copy import deepcopy
from typing import Protocol

from edgecloud_simulator.models import Allocation, ComputeNode, SimulationResult, Task


class AllocationStrategy(Protocol):
    name: str

    def choose_node(self, task: Task, nodes: list[ComputeNode]) -> ComputeNode | None:
        ...


def run_simulation(
    tasks: list[Task],
    nodes: list[ComputeNode],
    strategy: AllocationStrategy,
) -> SimulationResult:
    working_nodes = deepcopy(nodes)
    allocations: list[Allocation] = []

    for task in tasks:
        selected = strategy.choose_node(task, working_nodes)
        if selected is None:
            allocations.append(Allocation(task=task, node=None, reason="No feasible node found"))
            continue

        selected.allocate(task)
        allocations.append(Allocation(task=task, node=selected, reason="Allocated"))

    allocated = [allocation for allocation in allocations if allocation.node is not None]
    allocated_count = len(allocated)
    rejected_count = len(allocations) - allocated_count

    total_latency = sum(allocation.node.latency_ms for allocation in allocated if allocation.node)
    total_cost = sum(allocation.node.cost_per_task for allocation in allocated if allocation.node)
    total_energy = sum(allocation.node.energy_per_task for allocation in allocated if allocation.node)
    average_latency = total_latency / allocated_count if allocated_count else 0

    return SimulationResult(
        strategy_name=strategy.name,
        allocations=allocations,
        allocated_count=allocated_count,
        rejected_count=rejected_count,
        average_latency_ms=round(average_latency, 2),
        total_cost=round(total_cost, 2),
        total_energy=round(total_energy, 2),
    )
