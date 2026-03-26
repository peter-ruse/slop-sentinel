from dataclasses import dataclass


@dataclass
class StructuralNesting:
    max_nesting: int
    total_nesting: int
    total_statements: int
    average_nesting: float | None
