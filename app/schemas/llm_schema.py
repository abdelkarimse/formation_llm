from pydantic import BaseModel, Field
from typing import Optional, Literal

class LLMRequest(BaseModel):
    prompt: str = Field(..., example="Write a short story about AI.")
    model: Literal["ollama", 'nvidia',"ragwithollama",'ragwithnvidia'] 
class LLMResponse(BaseModel):
    response: str = Field(..., example="Once upon a time, AI...")
