from services import ollama_service
from services import rag_services
from services import nvidia_services


async def get_llm_response(prompt: str, model: str) -> str:
    if model.lower() == "ollama":
        return await ollama_service.ask(prompt)
    elif model.lower() == "nvidia":
        return await nvidia_services.ask(prompt)
    elif model.lower() == "ragwithollama":
        print("test")
        augment_prompt_withRetrivelData=rag_services.query_pdf(prompt)
        return await ollama_service.ask(augment_prompt_withRetrivelData)
    elif model.lower() == "ragwithnvidia":
        augment_prompt_withRetrivelData=rag_services.query_pdf(prompt)
        return await nvidia_services.ask(augment_prompt_withRetrivelData)
    else:
        print("test")
        return "Model not supported"
