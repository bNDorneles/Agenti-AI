import unittest

from edgecloud_simulator.models import ComputeNode, Task


class ComputeNodeTests(unittest.TestCase):
    def test_node_can_host_task_when_resources_and_latency_fit(self):
        node = ComputeNode(
            name="edge-1",
            kind="edge",
            cpu_capacity=8,
            memory_capacity=16,
            latency_ms=12,
            cost_per_task=0.2,
            energy_per_task=1.5,
        )
        task = Task(
            name="video-analytics",
            cpu_required=2,
            memory_required=4,
            max_latency_ms=20,
            priority=5,
        )

        self.assertTrue(node.can_host(task))

    def test_node_rejects_task_when_latency_is_too_high(self):
        node = ComputeNode(
            name="cloud",
            kind="cloud",
            cpu_capacity=32,
            memory_capacity=128,
            latency_ms=90,
            cost_per_task=0.05,
            energy_per_task=3.0,
        )
        task = Task(
            name="augmented-reality",
            cpu_required=2,
            memory_required=4,
            max_latency_ms=30,
            priority=5,
        )

        self.assertFalse(node.can_host(task))

    def test_allocate_consumes_available_resources(self):
        node = ComputeNode(
            name="edge-2",
            kind="edge",
            cpu_capacity=4,
            memory_capacity=8,
            latency_ms=10,
            cost_per_task=0.3,
            energy_per_task=1.0,
        )
        task = Task(
            name="sensor-filter",
            cpu_required=1,
            memory_required=2,
            max_latency_ms=25,
            priority=3,
        )

        node.allocate(task)

        self.assertEqual(node.cpu_used, 1)
        self.assertEqual(node.memory_used, 2)
        self.assertEqual(node.remaining_cpu, 3)
        self.assertEqual(node.remaining_memory, 6)


if __name__ == "__main__":
    unittest.main()
