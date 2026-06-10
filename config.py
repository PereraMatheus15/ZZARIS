import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
KNOWLEDGE_FILE = os.path.join(DATA_DIR, "knowledge.json")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
LOG_FILE = os.path.join(DATA_DIR, "logs.json")
EXAMPLES_FILE = os.path.join(BASE_DIR, "training", "examples.json")

VERSION = "0.1"
LEARNING_RATE = 0.5
DEFAULT_ACTIVATION = "sigmoid"
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]

# Ensure the data directory exists when the application starts
os.makedirs(DATA_DIR, exist_ok=True)
