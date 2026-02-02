from fastapi import FastAPI
from api import routes_llm, routes_health

app = FastAPI(title="LLM Server")

app.include_router(routes_llm.router, prefix="/llm", tags=["LLM"])
app.include_router(routes_health.router, prefix="/health", tags=["Health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
