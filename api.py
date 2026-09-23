from fastapi import FastAPI, HTTPException
#cors 에러 방지
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.genai._gaos.lib.compat_errors import RateLimitError

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
    try:
        result = run_agent(request.message)

        return {
            "result": result
        }

    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Gemini API 일일 요청 한도를 초과했습니다."
        )

    except Exception as e:
        print(f"[Agent Error] {e}")

        raise HTTPException(
            status_code=500,
            detail="Agent 요청 처리 중 오류가 발생했습니다."
        )