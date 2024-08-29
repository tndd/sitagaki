import json
from pathlib import Path

MOCK_ROOT = Path(__file__).parent

def load(filename: str) -> dict:
    file_path = MOCK_ROOT / filename
    with file_path.open('r') as f:
        return json.load(f)