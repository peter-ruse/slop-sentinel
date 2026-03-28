from pydantic import BaseModel


class LexicalDiversity(BaseModel):
    unique_identifiers: int
    total_identifiers: int
    score: float | None
