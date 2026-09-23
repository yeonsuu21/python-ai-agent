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
    #내부에 있는 에이전트에 메세지 전송
    return {
        "result": result
    }