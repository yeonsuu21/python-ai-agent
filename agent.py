import json
import os

from dotenv import load_dotenv
from google import genai

from tools import (
    get_schedule,
    get_employee,
    calculate_workload,
    create_email_draft,
)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


TOOLS = [
    {
        "type": "function",
        "name": "get_schedule",
        "description": "특정 기간의 공연 일정을 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "조회 시작 날짜 YYYY-MM-DD",
                },
                "end_date": {
                    "type": "string",
                    "description": "조회 종료 날짜 YYYY-MM-DD",
                },
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "type": "function",
        "name": "get_employee",
        "description": "이름으로 담당자 정보를 조회합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "담당자 이름",
                }
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "calculate_workload",
        "description": "담당자의 업무량을 계산합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee": {
                    "type": "string",
                    "description": "담당자 이름",
                }
            },
            "required": ["employee"],
        },
    },
    {
    "type": "function",
    "name": "create_email_draft",
    "description": "담당자에게 보낼 공연 일정 안내 이메일 초안을 생성합니다.",
    "parameters": {
        "type": "object",
        "properties": {
            "employee": {
                "type": "string",
                "description": "이메일을 받을 담당자 이름"
            },
            "schedules": {
                "type": "array",
                "description": "이메일에 포함할 담당자의 공연 일정",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string"
                        },
                        "performance": {
                            "type": "string"
                        },
                        "manager": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "required": ["employee", "schedules"]
    }
}
]


TOOL_FUNCTIONS = {
    "get_schedule": get_schedule,
    "get_employee": get_employee,
    "calculate_workload": calculate_workload,
    "create_email_draft": create_email_draft,
}


def run_agent(user_input):

    history = [
        {
            "type": "user_input",
            "content": [
                {
                    "type": "text",
                    "text": user_input
                }
            ],
        }
    ]

    while True:

        response = client.interactions.create(
            model="gemini-3.8-flash",
            store=False,
            input=history,
            tools=TOOLS,
        )

        # Gemini가 생성한 판단/Tool Call을 history에 저장
        for step in response.steps:
            history.append(step.model_dump())

        tool_called = False

        for step in response.steps:

            if step.type != "function_call":
                continue

            tool_called = True

            tool_name = step.name
            arguments = step.arguments

            print(f"\n[Agent] Tool 선택: {tool_name}")
            print(f"[Agent] Arguments: {arguments}")

            function = TOOL_FUNCTIONS[tool_name]

            result = function(**arguments)

            print(f"[Tool Result] {result}")

            # Tool 실행 결과를 다시 Gemini에게 전달
            history.append(
                {
                    "type": "function_result",
                    "name": tool_name,
                    "call_id": step.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                result,
                                ensure_ascii=False
                            ),
                        }
                    ],
                }
            )

        if not tool_called:
            return response.output_text