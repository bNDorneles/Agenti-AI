from __future__ import annotations

from edgecloud_simulator.models import ComputeNode, Task


def build_demo_scenario() -> tuple[list[Task], list[ComputeNode]]:
    tasks = [
        Task("ar-frame-processing", 2, 4, 25, 5),
        Task("traffic-camera-ai", 3, 6, 35, 5),
        Task("sensor-filtering", 1, 2, 40, 3),
        Task("batch-report", 4, 8, 120, 1),
        Task("predictive-maintenance", 5, 10, 90, 3),
        Task("emergency-alert", 2, 3, 20, 5),
        Task("log-compression", 2, 4, 150, 1),
        Task("robot-control-loop", 3, 3, 15, 5),
    ]

    nodes = [
        ComputeNode("edge-a", "edge", 6, 12, 12, 0.28, 1.1),
        ComputeNode("edge-b", "edge", 5, 10, 18, 0.24, 1.0),
        ComputeNode("regional-cloud", "cloud", 16, 64, 65, 0.12, 2.8),
        ComputeNode("central-cloud", "cloud", 32, 128, 95, 0.08, 3.4),
    ]

    return tasks, nodes
