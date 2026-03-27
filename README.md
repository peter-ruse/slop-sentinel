# Slop Sentinel

This is a FastAPI app that computes "slop" metrics for Python projects. Post a repository link to `/slop_metrics` and get back JSON with a summary of slop metrics. (You'll need to use your own GitHub API token, of course.) More features coming soon.

**Note**: Currently only GitHub links are supported.

## The Slop Metrics
### Cyclomatic Complexity
- The cyclomatic complexity of a function is the number of linearly independent paths through its Control Flow Graph. The smaller the score, the better.

### Structural Nesting
- Structural nesting is a measure of the amount of nesting due to statements of type `if`, `for`, `async for`, `while`, `try`, `with`, or `async with`. Our slop detection engine computes max nesting and average nesting across the codebase. The smaller the score, the better.

### Lexical Diversity
- The lexical diversity of a codebase is the number of unique identifiers (variables, functions, classes) divided by the total number of identifiers. Scores between 0.3 and 0.7 are ideal: low values tend to indicate repetitive boilerplate, while high values usually indicate inconsistent naming.

## Technical Implementation: `ast`
The implementation uses Python's `ast` (Abstract Syntax Tree) module. To better understand how the `ast` visitors work:

- The `visit` method on an `ast.NodeVisitor` delegates to specific handlers (e.g., `visit_If` or `visit_FunctionDef`) depending on the node type.
- The `generic_visit` recursively calls `visit` on each of the children of the current node, enabling us to recursively visit the entire tree.

By overriding these methods accordingly, we're able to traverse the syntax tree and collect the data required to compute our metrics.