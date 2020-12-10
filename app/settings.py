import os
from dotenv import load_dotenv
import logging


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
load_dotenv(verbose=True, dotenv_path=os.path.join(PROJECT_ROOT, '.env'))

SERVICE_ID = os.getenv('SERVICE_ID')
SERVICE_ADDRESS = os.getenv('SERVICE_ADDRESS')
SERVICE_PORT = os.getenv('SERVICE_PORT')

CACHE_RAM_QUOTA_MB = os.getenv('CACHE_RAM_QUOTA_MB')
CACHE_DISK_QUOTA_MB = os.getenv('CACHE_DISK_QUOTA_MB')
LP_DATA_DIR = os.getenv('LP_DATA_DIR')

LOG_LEVEL = logging.DEBUG
