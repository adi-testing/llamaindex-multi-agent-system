import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Model settings
LLM_TYPE = "local"
LOCAL_LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "not-needed-for-local")

# For local LLM
LOCAL_LLM_MODEL = "mistral-7b-instruct-v0.3"

# For OpenAI
OPENAI_LLM_MODEL = "gpt-3.5-turbo"

# Default embedding model (works locally)
EMBEDDING_MODEL = "local:BAAI/bge-small-en-v1.5"

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
KB_PERSIST_DIR = PROJECT_ROOT / "storage" / "knowledge_base"

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
