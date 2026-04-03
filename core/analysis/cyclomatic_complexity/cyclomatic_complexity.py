import ast

from core.analysis.base import BaseVisitor
from core.analysis.cyclomatic_complexity.models import (
    CyclomaticComplexity,
    FunctionComplexity,
)
from core.analysis.enums import MetricName


class CyclomaticComplexityVisitor(BaseVisitor):
    metric_name = MetricName.CYCLOMATIC_COMPLEXITY

    def __init__(self):
        self.complexities: list[FunctionComplexity] = []

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        decision_point_visitor = DecisionPointVisitor()
        decision_point_visitor.generic_visit(node)
        complexity = 1 + decision_point_visitor.count
        self.complexities.append(
            FunctionComplexity(
                name=f"{self.module_fqn}.{node.name}", complexity=complexity
            )
        )
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._visit_function(node)

    def compute_results(self):
        if not self.complexities:
            return CyclomaticComplexity(
                max=None, mean=None, total_functions=0, worst=[]
            )

        complexities = [c.complexity for c in self.complexities]
        worst = sorted(self.complexities, key=lambda c: -c.complexity)[:10]

        return CyclomaticComplexity(
            max=max(complexities),
            mean=sum(complexities) / len(complexities),
            total_functions=len(complexities),
            worst=worst,
        )


class DecisionPointVisitor(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_If(self, node: ast.If):
        self.count += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.count += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self.count += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.count += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.count += len(node.values) - 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        self.count += 1
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        self.count += 1
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension):
        self.count += 1 + len(node.ifs)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef): ...

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef): ...

    def visit_ClassDef(self, node: ast.ClassDef): ...
