import unittest

from edgecloud_simulator.models import ComputeNode, Task
from edgecloud_simulator.strategies import BaselineStrategy, SmartStrategy


class StrategyTests(unittest.TestCase):
    def test_baseline_chooses_first_feasible_node(self):
        task = Task("batch-report", 2, 4, 100, 2)
        nodes = [
            ComputeNode("edge-full", "edge", 1, 16, 10, 0.3, 1.0),
            ComputeNode("edge-ok", "edge", 4, 16, 12, 0.3, 1.1),
            ComputeNode("cloud-ok", "cloud", 32, 128, 80, 0.1, 3.5),
        ]

        selected = BaselineStrategy().choose_node(task, nodes)

        self.assertEqual(selected.name, "edge-ok")

    def test_smart_strategy_prefers_low_latency_for_high_priority_task(self):
        task = Task("ar-frame", 2, 2, 120, 5)
        nodes = [
            ComputeNode("cheap-cloud", "cloud", 32, 128, 85, 0.05, 3.0),
            ComputeNode("near-edge", "edge", 8, 16, 10, 0.25, 1.2),
        ]

        selected = SmartStrategy().choose_node(task, nodes)

        self.assertEqual(selected.name, "near-edge")

    def test_smart_strategy_returns_none_when_no_node_is_feasible(self):
        task = Task("strict-control", 2, 2, 5, 5)
        nodes = [
            ComputeNode("edge", "edge", 8, 16, 10, 0.25, 1.2),
            ComputeNode("cloud", "cloud", 32, 128, 80, 0.05, 3.0),
        ]

        selected = SmartStrategy().choose_node(task, nodes)

        self.assertIsNone(selected)


if __name__ == "__main__":
    unittest.main()
