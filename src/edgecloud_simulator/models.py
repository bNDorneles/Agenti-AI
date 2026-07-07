from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Task:
    name: str
    cpu_required: float
    memory_required: float
    max_latency_ms: float
    priority: int


@dataclass
class ComputeNode:
    name: str
    kind: str
    cpu_capacity: float
    memory_capacity: float
    latency_ms: float
    cost_per_task: float
    energy_per_task: float
    cpu_used: float = 0
    memory_used: float = 0

    @property
    def remaining_cpu(self) -> float:
        return self.cpu_capacity - self.cpu_used

    @property
    def remaining_memory(self) -> float:
        return self.memory_capacity - self.memory_used

    def can_host(self, task: Task) -> bool:
        has_cpu = self.remaining_cpu >= task.cpu_required
        has_memory = self.remaining_memory >= task.memory_required
        meets_latency = self.latency_ms <= task.max_latency_ms
        return has_cpu and has_memory and meets_latency

    def allocate(self, task: Task) -> None:
        if not self.can_host(task):
            raise ValueError(f"Node {self.name} cannot host task {task.name}")
        self.cpu_used += task.cpu_required
        self.memory_used += task.memory_required


@dataclass(frozen=True)
class Allocation:
    task: Task
    node: ComputeNode | None
    reason: str


@dataclass(frozen=True)
class SimulationResult:
    strategy_name: str
    allocations: list[Allocation] = field(default_factory=list)
    allocated_count: int = 0
    rejected_count: int = 0
    average_latency_ms: float = 0
    total_cost: float = 0
    total_energy: float = 0
