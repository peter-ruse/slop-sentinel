from enum import StrEnum

from pydantic import BaseModel

from core.analysis.cyclomatic_complexity.models import CyclomaticComplexity
from core.analysis.lexical_diversity.models import LexicalDiversity
from core.analysis.structural_nesting.models import StructuralNesting


class MetricName(StrEnum):
    LEXICAL_DIVERSITY = "lexical_diversity"
    CYCLOMATIC_COMPLEXITY = "cyclomatic_complexity"
    STRUCTURAL_NESTING = "structural_nesting"


class AnalysisResults(BaseModel):
    results: dict[str, LexicalDiversity | CyclomaticComplexity | StructuralNesting]
