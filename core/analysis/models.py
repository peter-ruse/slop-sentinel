from pydantic import BaseModel

from core.analysis.cyclomatic_complexity.models import CyclomaticComplexity
from core.analysis.lexical_diversity.models import LexicalDiversity
from core.analysis.structural_nesting.models import StructuralNesting


class AnalysisResults(BaseModel):
    results: dict[str, LexicalDiversity | CyclomaticComplexity | StructuralNesting]
