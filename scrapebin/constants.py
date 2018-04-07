import os

PROJECT_ROOT = os.path.join(os.path.realpath(os.path.abspath(os.path.dirname(__file__))), '..')
BACKUP_DIR = os.path.join(PROJECT_ROOT, 'backup')
DATA_DIR = os.path.join(PROJECT_ROOT, 'pastes')
CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config.ini')
PASTES_PER_REQUEST = 100
SLEEP_DURATION = 120
