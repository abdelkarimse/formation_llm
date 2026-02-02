# app/main.py
from fastapi import FastAPI
from api import routes_llm, routes_health
from utils.logger import logger 

app = FastAPI(title="LLM Server")

app.include_router(routes_llm.router, prefix="/llm", tags=["LLM"])
app.include_router(routes_health.router, prefix="/health", tags=["Health"])

@app.on_event("startup")
async def startup_event():
    logger.info("LLM Server is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("LLM Server is shutting down...")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server at 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
