from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.agents.agent import AutomationAgent
from app.tools.email_tool import EmailTool
from app.tools.task_tool import TaskTool

app = FastAPI(
    title="AI Email & Task Automation Agent",
    version="1.0.0",
    description="Safe, local agentic automation for everyday work tasks.",
)

agent = AutomationAgent(
    email_tool=EmailTool(),
    task_tool=TaskTool(),
)


class AgentRequest(BaseModel):
    request: str = Field(min_length=3)


class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str


class TaskRequest(BaseModel):
    title: str
    due: str | None = None


@app.get("/health")
def health():
    return {"status": "ok", "agent": "ready", "mode": "local-zero-key"}


@app.post("/api/agent/run")
def run_agent(payload: AgentRequest):
    return agent.run(payload.request)


@app.post("/api/email/draft")
def draft_email(payload: EmailRequest):
    return EmailTool().draft(
        to=payload.to,
        subject=payload.subject,
        body=payload.body,
    )


@app.post("/api/tasks")
def create_task(payload: TaskRequest):
    return TaskTool().create(title=payload.title, due=payload.due)
