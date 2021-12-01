import sys
from pathlib import Path

root = Path()
root = f"{root.cwd()}/autorok"
sys.path.append(root)
from autorok import *
