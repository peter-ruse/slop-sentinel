import ast

from core.analysis.base import BaseVisitor
from core.analysis.cyclomatic_complexity.models import (
    CyclomaticComplexity,
    FunctionComplexity,
)
from core.analysis.models import MetricName


class CyclomaticComplexityVisitor(BaseVisitor):
    metric_name = MetricName.CYCLOMATIC_COMPLEXITY

    def __init__(self):
        self.complexities: list[FunctionComplexity] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._visit_function(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        local_visitor = DecisionPointVisitor()
        for child in node.body:
            local_visitor.visit(child)
        complexity = 1 + local_visitor.count
        self.complexities.append(
            FunctionComplexity(
                name=f"{self.module_fqn}.{node.name}", complexity=complexity
            )
        )
        self.generic_visit(node)

    def compute_results(self):
        if not self.complexities:
            return CyclomaticComplexity(0.0, 0, 0, [])

        complexities = [c.complexity for c in self.complexities]
        worst = sorted(self.complexities, key=lambda c: -c.complexity)[:10]

        return CyclomaticComplexity(
            mean=sum(complexities) / len(complexities),
            max_complexity=max(complexities),
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

    def visit_While(self, node: ast.While):
        self.count += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        self.count += len(node.values) - 1
        self.generic_visit(node)
