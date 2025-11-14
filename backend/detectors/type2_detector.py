import ast
import difflib

class Normalizer(ast.NodeTransformer):
    """AST transformer to normalize variable, function, and class names."""
    def visit_Name(self, node):
        # Replace all variable names with generic placeholder
        return ast.copy_location(ast.Name(id="VAR", ctx=node.ctx), node)

    def visit_FunctionDef(self, node):
        # Replace function names and recursively normalize inside
        node.name = "FUNC"
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        # Replace class names
        node.name = "CLASS"
        self.generic_visit(node)
        return node


def normalize_code_ast(code: str) -> str:
    """
    Convert code into normalized AST representation string.
    All variable/function/class names replaced with placeholders.
    """
    try:
        tree = ast.parse(code)
        normalizer = Normalizer()
        normalized_tree = normalizer.visit(tree)
        ast.fix_missing_locations(normalized_tree)
        # dump() converts AST to string form
        return ast.dump(normalized_tree)
    except Exception:
        # If code can’t be parsed, fallback to raw text
        return code


def type2_similarity(code1: str, code2: str) -> float:
    """
    Compute structural similarity using normalized ASTs and difflib.
    """
    norm1, norm2 = normalize_code_ast(code1), normalize_code_ast(code2)
    matcher = difflib.SequenceMatcher(None, norm1, norm2)
    return round(matcher.ratio() * 100, 2)
