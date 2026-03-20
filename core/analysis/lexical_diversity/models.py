from dataclasses import dataclass


@dataclass
class LexicalDiversity:
    unique_identifiers: int
    total_identifiers: int
    score: float
