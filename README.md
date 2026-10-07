# AI Email & Task Automation Agent

A portfolio-ready agentic AI project that turns natural-language work requests into safe, ordered actions.

## What it does

The agent can:
- Draft professional emails
- Create tasks/reminders
- Inspect task state
- Execute multi-step workflows
- Handle follow-up actions when a tool succeeds or fails
- Run without any paid API key in deterministic demo mode

Example request:

> Draft a follow-up email to Sarah about the interview and remind me tomorrow at 10 AM to send it.

The planner decomposes this into:
1. Draft the email
2. Create a reminder
3. Return an execution summary

## Architecture

```text
User Request
    |
    v
Intent / Planner
    |
    v
Execution Plan
    |
    +--> Email Tool ------> email_drafts.json
    |
    +--> Task Tool -------> tasks.json
    |
    +--> Follow-up / Recovery
    |
    v
Structured Result
```

The project deliberately uses a local rule-based planner by default, so the full demo works with **zero API keys**. An LLM provider can be added later behind the planner interface.

## Stack

- Python 3.12+
- FastAPI
- Pydantic
- LangChain-compatible agent architecture
- SQLite-free JSON tool storage for a simple zero-key demo
- Pytest
- Optional Docker

## Run

```powershell
cd "F:\MY PROJECTS\ai-email-task-automation-agent"
uv venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## API

### POST /api/agent/run

```json
{
  "request": "Draft an email to Sarah about the interview and remind me tomorrow at 10 AM to send it."
}
```

### POST /api/email/draft

```json
{
  "to": "sarah@example.com",
  "subject": "Interview Follow-up",
  "body": "Thank you for the opportunity..."
}
```

### POST /api/tasks

```json
{
  "title": "Send interview follow-up",
  "due": "tomorrow 10:00"
}
```

## Safety model

The demo agent does not send real email or create external calendar events. It creates local drafts/tasks and reports exactly what it did. This makes the project safe to run locally and easy to demonstrate.

## Optional LLM upgrade

The planner is isolated in `app/agents/planner.py`. You can replace `RuleBasedPlanner` with an LLM-backed planner later without changing the tools or API contract.

## Tests

```powershell
pytest -q
```

## Resume bullet

**AI Email & Task Automation Agent** — Python, FastAPI, Agentic AI, Pydantic, Tool Calling, Workflow Planning, Pytest  
Built an agentic workflow engine that converts natural-language work requests into ordered email-drafting and task-reminder actions, with tool selection, execution tracking, and failure recovery; designed a zero-API-key local mode for safe automation demos.
