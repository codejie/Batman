"""
Utility functions for EastMoney library.
"""

def get_secid(code: str) -> str:
    """
    Generate EastMoney secid from stock code.
    SH (6xxxxx) -> 1.code
    SZ (0xxxxx, 3xxxxx) -> 0.code
    BJ (8xxxxx, 4xxxxx) -> 0.code (Usually 0 for BJ in some contexts, but let's assume 0 for non-6)
    """
    if str(code).startswith('6'):
        return f"1.{code}"
    elif str(code).startswith('9'): # B share SH?
         return f"1.{code}"
    else:
        return f"0.{code}"

def get_secids(codes: list[str]) -> str:
    """
    Generate comma-separated secids string.
    """
    return ",".join([get_secid(c) for c in codes])
