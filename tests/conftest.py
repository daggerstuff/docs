import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINEAR_AUDIT = ROOT / "linear-audit"

sys.path.insert(0, str(LINEAR_AUDIT))
