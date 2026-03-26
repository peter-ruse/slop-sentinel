# Slop Sentinel

This is a FastAPI project that computes "slop" metrics for public Python projects. Give it a repository link (only GitHub is currently supported, and of course you need to use your own API token), and get back json with a summary of slop metrics. More features to come.

## The Slop Metrics
### Cyclomatic Complexity
- The cyclomatic complexity of a function is the number of linearly independent paths through its Control Flow Graph. The smaller the score, the better.

### Structural Nesting
- Structural nesting is a measure of the amount of nesting, due to statements of type `if`, `for`, `async for`, `while`, `try`, `with`, `async with`. Here we compute max nesting and average nesting across the codebase. The smaller the score, the better.

### Lexical Diversity
- The lexical diversity of a codebase is the number of unique idenfiers (variables, functions, classes) divided by the total number of identifiers. Scores between 0.3 and 0.7 are ideal. Low values indicate extreme redundancy, while high values indicate inconsistent naming conventions.

## Python's ast module
To better understand the code, note
- The `visit` method on a `ast.NodeVisitor` delegates to one of its `visit_<NodeType>` methods (e.g., `visit_If` or `visit_FunctionDef`) depending on the type of the node.
- The `generic_visit` method is used to continue down the tree: it calls `visit` on each of the children of the node.