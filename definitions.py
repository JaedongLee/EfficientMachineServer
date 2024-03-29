import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CLIENT_ROOT_DIR = f'{Path(__file__).resolve().parents[2]}//Client'

TOOLS_DOWNLOAD_DIRECTORY = '{client_root_dir}/EfficientMachine/EfficientMachine/Resources/Tools/Program' \
        .format(client_root_dir=CLIENT_ROOT_DIR)