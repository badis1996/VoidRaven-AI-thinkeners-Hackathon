import base64
from pathlib import Path

def get_test_cv_base64() -> str:
    """Get the test CV file as base64 encoded string."""
    cv_path = Path(__file__).parent / "cvexamples" / "Madrid-Resume-Template-Modern.pdf"
    with open(cv_path, "rb") as f:
        return base64.b64encode(f.read()).decode() 