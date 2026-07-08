import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dashboard import build_allocation_rows, build_summary_rows
from edgecloud_simulator.models import Allocation, ComputeNode, SimulationResult, Task


class DashboardDataTests(unittest.TestCase):
    def test_build_summary_rows_translates_metrics_to_portuguese_columns(self):
        result = SimulationResult(
            strategy_name="smart",
            allocated_count=2,
            rejected_count=1,
            average_latency_ms=18.5,
            total_cost=0.52,
            total_energy=2.1,
        )

        rows = build_summary_rows([result])

        self.assertEqual(
            rows,
            [
                {
                    "Estrategia": "smart",
                    "Tarefas alocadas": 2,
                    "Tarefas rejeitadas": 1,
                    "Latencia media (ms)": 18.5,
                    "Custo total": 0.52,
                    "Energia total": 2.1,
                }
            ],
        )

    def test_build_allocation_rows_handles_allocated_and_rejected_tasks(self):
        task_a = Task("sensor-filtering", 1, 2, 40, 3)
        task_b = Task("robot-control-loop", 3, 3, 15, 5)
        node = ComputeNode("edge-a", "edge", 6, 12, 12, 0.28, 1.1)
        result = SimulationResult(
            strategy_name="baseline",
            allocations=[
                Allocation(task=task_a, node=node, reason="Allocated"),
                Allocation(task=task_b, node=None, reason="No feasible node found"),
            ],
        )

        rows = build_allocation_rows([result])

        self.assertEqual(rows[0]["Estrategia"], "baseline")
        self.assertEqual(rows[0]["Tarefa"], "sensor-filtering")
        self.assertEqual(rows[0]["No escolhido"], "edge-a")
        self.assertEqual(rows[0]["Tipo do no"], "edge")
        self.assertEqual(rows[0]["Status"], "Alocada")
        self.assertEqual(rows[0]["Motivo"], "Alocada com sucesso")
        self.assertEqual(rows[1]["No escolhido"], "-")
        self.assertEqual(rows[1]["Tipo do no"], "-")
        self.assertEqual(rows[1]["Status"], "Rejeitada")
        self.assertEqual(rows[1]["Motivo"], "Nenhum no viavel encontrado")


if __name__ == "__main__":
    unittest.main()
