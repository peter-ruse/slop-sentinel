from pydantic import BaseModel


class FunctionComplexity(BaseModel):
    name: str
    complexity: int


class CyclomaticComplexity(BaseModel):
    max: int | None
    mean: float | None
    total_functions: int
    worst: list[FunctionComplexity]
