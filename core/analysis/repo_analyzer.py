import ast
from typing import Iterable

from core.analysis.base import BaseVisitor


class RepoAnalyzer:
    def __init__(self, visitors: list[BaseVisitor]):
        self.visitors = visitors

    def consolidate_results(self, trees: Iterable[tuple[str, ast.AST]]):
        for module_fqn, tree in trees:
            for visitor in self.visitors:
                visitor.update_module_fqn(module_fqn)
                visitor.visit(tree)

        results = dict()
        for visitor in self.visitors:
            results[visitor.metric_name] = visitor.compute_results()

        return results
