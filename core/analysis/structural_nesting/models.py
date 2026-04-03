from pydantic import BaseModel


class StructuralNesting(BaseModel):
    max: int
    mean: float | None
    total_nesting: int
    total_statements: int
