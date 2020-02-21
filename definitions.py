"""
This file contains important project variables.
"""
import os
from pathlib import Path

# This sets our root directory as the project directory
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))  # This is your Project Root

DIR_DATA = ROOT_DIR / "data"
