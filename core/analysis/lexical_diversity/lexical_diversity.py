import ast

from core.analysis.base import BaseVisitor
from core.analysis.lexical_diversity.models import LexicalDiversity
from core.analysis.models import MetricName


class LexicalDiversityVisitor(BaseVisitor):
    metric_name = MetricName.LEXICAL_DIVERSITY

    def __init__(self):
        self.identifiers = []

    def visit_Name(self, node: ast.Name):
        self.identifiers.append(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.identifiers.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.identifiers.append(node.name)
        self.generic_visit(node)

    def compute_results(self) -> LexicalDiversity:
        if not self.identifiers:
            return LexicalDiversity(
                unique_identifiers=0, total_identifiers=0, score=None
            )

        unique_identifiers = len(set(self.identifiers))
        total_identifiers = len(self.identifiers)

        return LexicalDiversity(
            unique_identifiers=unique_identifiers,
            total_identifiers=total_identifiers,
            score=unique_identifiers / total_identifiers,
        )
