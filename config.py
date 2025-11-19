import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Default data files
DEFAULT_DATA_FILE = os.path.join(DATA_DIR, "issuu_cw2.json")
SAMPLE_DATA_FILE = os.path.join(DATA_DIR, "issuu_sample.json")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)