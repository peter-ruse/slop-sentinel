from dataclasses import dataclass


@dataclass
class FunctionComplexity:
    name: str
    complexity: int


@dataclass
class CyclomaticComplexity:
    mean: float
    max_complexity: int
    total_functions: int
    worst: list[FunctionComplexity]
