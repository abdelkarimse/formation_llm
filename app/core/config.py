import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file automatically

class Settings:
    model_name_ollama: str = os.environ.get("MODEL_NAME_OLLAMA", "qwen3:4b")
    embedding_ollama: str = os.environ.get("Embedding_OLLAMA", "nomic-embed-text:latest")
    nvidia_key: str = os.environ.get("NVIDIA_API_KEY", "")  

settings = Settings()
