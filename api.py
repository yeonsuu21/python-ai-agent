from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent


app = FastAPI()


class AgentRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "AI Agent API is running"
    }


@app.post("/agent")
def agent(request: AgentRequest):
    result = run_agent(request.message)

    return {
        "result": result
    }