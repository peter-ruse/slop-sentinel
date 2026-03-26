from dataclasses import dataclass


@dataclass
class FunctionComplexity:
    name: str
    complexity: int


@dataclass
class CyclomaticComplexity:
    mean: float | None
    max_complexity: int | None
    total_functions: int
    worst: list[FunctionComplexity]
