import sys
from typeguard.importhook import install_import_hook
from pathlib import Path

root = Path()
root = f"{root.cwd()}/autorok"
sys.path.append(root)

# Install import hook
install_import_hook('autorok')

from autorok import *
