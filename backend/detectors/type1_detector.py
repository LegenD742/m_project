import re

def normalize_code_type1(code: str) -> str:
    """Removes comments and whitespace to compare structural equality."""
    # Remove single-line comments
    code = re.sub(r"#.*", "", code)          # Python
    code = re.sub(r"//.*", "", code)         # C++, Java, JS
    # Remove multi-line comments
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    # Remove all whitespace
    code = re.sub(r"\s+", "", code)
    return code.strip()

def type1_similarity(code1: str, code2: str) -> float:
    """Returns 100 if identical after normalization, else 0."""
    n1, n2 = normalize_code_type1(code1), normalize_code_type1(code2)
    return 100.0 if n1 == n2 else 0.0
