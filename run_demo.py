from app.agents.agent import AutomationAgent
from app.tools.email_tool import EmailTool
from app.tools.task_tool import TaskTool
import json

agent = AutomationAgent(EmailTool(), TaskTool())

request = (
    "Draft an email to hiring@example.com about my interview "
    "and remind me tomorrow at 10 AM to send it."
)

print(json.dumps(agent.run(request), indent=2))
