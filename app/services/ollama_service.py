from langchain_community.llms import Ollama
from core.config import settings

llm = Ollama(
    model=settings.model_name_ollama,
    base_url="http://127.0.0.1:11434" 
)

async def ask(prompt: str) -> str:
    response = await llm.ainvoke(prompt)
    return response
