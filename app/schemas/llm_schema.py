from pydantic import BaseModel, Field
from typing import Optional, Literal

class LLMRequest(BaseModel):
    prompt: str = Field(..., example="Write a short story about AI.")
    model: Literal["ollama", "gemini"] = Field(
        default="ollama", 
        example="ollama",
        description="Choose the model to use: ollama, gemini",
        
    )    
class LLMResponse(BaseModel):
    response: str = Field(..., example="Once upon a time, AI...")
