from __future__ import annotations

from edgecloud_simulator.models import ComputeNode, Task

RESOURCE_PRESSURE_WEIGHT = 20
COST_WEIGHT = 15
ENERGY_WEIGHT = 4


class BaselineStrategy:
    name = "baseline"

    def choose_node(self, task: Task, nodes: list[ComputeNode]) -> ComputeNode | None:
        for node in nodes:
            if node.can_host(task):
                return node
        return None


class SmartStrategy:
    name = "smart"

    def choose_node(self, task: Task, nodes: list[ComputeNode]) -> ComputeNode | None:
        feasible_nodes = [node for node in nodes if node.can_host(task)]
        if not feasible_nodes:
            return None
        return min(feasible_nodes, key=lambda node: self.score(task, node))

    def score(self, task: Task, node: ComputeNode) -> float:
        priority_weight = 1 + (task.priority / 5)
        latency_component = node.latency_ms * priority_weight
        resource_pressure = self._resource_pressure(task, node) * RESOURCE_PRESSURE_WEIGHT
        cost_component = node.cost_per_task * COST_WEIGHT
        energy_component = node.energy_per_task * ENERGY_WEIGHT
        return latency_component + resource_pressure + cost_component + energy_component

    def _resource_pressure(self, task: Task, node: ComputeNode) -> float:
        cpu_after = (node.cpu_used + task.cpu_required) / node.cpu_capacity
        memory_after = (node.memory_used + task.memory_required) / node.memory_capacity
        return (cpu_after + memory_after) / 2
