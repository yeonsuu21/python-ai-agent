from fastapi import FastAPI
#cors 에러 방지
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import run_agent



app = FastAPI()

#cors 에러 방지
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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