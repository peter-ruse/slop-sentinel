import ast
from typing import Protocol

from core.analysis.enums import MetricName


class VisitorProtocol(Protocol):
    metric_name: MetricName

    def compute_results(self): ...


class BaseVisitor(ast.NodeVisitor, VisitorProtocol):
    def update_module_fqn(self, module_fqn: str):
        self.module_fqn = module_fqn
