import ast

from core.analysis.base import BaseVisitor
from core.analysis.models import MetricName
from core.analysis.structural_nesting.models import StructuralNesting


class StructuralNestingVisitor(BaseVisitor):
    metric_name = MetricName.STRUCTURAL_NESTING

    def __init__(self):
        self.max_nesting = 0
        self.total_nesting = 0
        self.total_statements = 0
        self.current_nesting = 0

    def _visit_nesting_node(self, node: ast.AST):
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1

    def visit_If(self, node: ast.If):
        self._visit_nesting_node(node)

    def visit_For(self, node: ast.For):
        self._visit_nesting_node(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self._visit_nesting_node(node)

    def visit_While(self, node: ast.While):
        self._visit_nesting_node(node)

    def visit_Try(self, node: ast.Try):
        self._visit_nesting_node(node)

    def visit_With(self, node: ast.With):
        self._visit_nesting_node(node)

    def visit_AsyncWith(self, node: ast.AsyncWith):
        self._visit_nesting_node(node)

    def visit(self, node: ast.AST):
        if isinstance(node, ast.stmt) and not isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            self.total_nesting += self.current_nesting
            self.total_statements += 1
        super().visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_nesting = self.current_nesting
        self.current_nesting = 0
        self.generic_visit(node)
        self.current_nesting = old_nesting

    def compute_results(self) -> StructuralNesting:
        if self.total_statements == 0:
            return StructuralNesting(
                total_nesting=0, total_statements=0, max=0, mean=None
            )

        return StructuralNesting(
            total_nesting=self.total_nesting,
            total_statements=self.total_statements,
            max=self.max_nesting,
            mean=self.total_nesting / self.total_statements,
        )
