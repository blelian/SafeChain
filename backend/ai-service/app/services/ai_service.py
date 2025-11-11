def analyze_password(password: str) -> int:
    """
    Dummy AI function that returns a score 0-100
    Replace with PyTorch / ML model logic later
    """
    return min(max(len(password) * 10, 0), 100)
