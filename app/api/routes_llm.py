
from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_router import get_llm_response
from schemas.llm_schema import LLMRequest, LLMResponse

router = APIRouter()



@router.post("/ask", response_model=LLMResponse)
async def ask_llm(request: LLMRequest):
    result = await get_llm_response(request.prompt, request.model)
    return {"response": result}
