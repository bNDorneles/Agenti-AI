import unittest

from edgecloud_simulator.models import ComputeNode, Task
from edgecloud_simulator.simulator import run_simulation
from edgecloud_simulator.strategies import BaselineStrategy


class SimulatorTests(unittest.TestCase):
    def test_run_simulation_allocates_tasks_and_computes_metrics(self):
        tasks = [
            Task("sensor-filter", 1, 2, 30, 3),
            Task("batch-report", 2, 4, 100, 1),
        ]
        nodes = [
            ComputeNode("edge", "edge", 4, 8, 10, 0.2, 1.0),
            ComputeNode("cloud", "cloud", 16, 64, 70, 0.1, 3.0),
        ]

        result = run_simulation(tasks, nodes, BaselineStrategy())

        self.assertEqual(result.allocated_count, 2)
        self.assertEqual(result.rejected_count, 0)
        self.assertEqual(result.average_latency_ms, 10)
        self.assertEqual(result.total_cost, 0.4)
        self.assertEqual(result.total_energy, 2.0)

    def test_run_simulation_rejects_task_when_no_node_can_host_it(self):
        tasks = [Task("robot-control", 2, 2, 5, 5)]
        nodes = [ComputeNode("edge", "edge", 4, 8, 10, 0.2, 1.0)]

        result = run_simulation(tasks, nodes, BaselineStrategy())

        self.assertEqual(result.allocated_count, 0)
        self.assertEqual(result.rejected_count, 1)
        self.assertIsNone(result.allocations[0].node)
        self.assertIn("No feasible node", result.allocations[0].reason)


if __name__ == "__main__":
    unittest.main()
