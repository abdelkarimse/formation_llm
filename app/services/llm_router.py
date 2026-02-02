from services import ollama_service, gemini_service

async def get_llm_response(prompt: str, model: str) -> str:
    if model.lower() == "ollama":
        return await ollama_service.ask(prompt)
    elif model.lower() == "gemini":
        return await gemini_service.ask(prompt)
    else:
        return "Model not supported"
