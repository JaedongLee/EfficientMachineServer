import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CLIENT_ROOT_DIR = f'{Path(__file__).resolve().parents[1]}//Client'
