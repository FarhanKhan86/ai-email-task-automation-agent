from app.agents.planner import RuleBasedPlanner
from app.tools.email_tool import EmailTool
from app.tools.task_tool import TaskTool


class AutomationAgent:
    def __init__(
        self,
        email_tool: EmailTool,
        task_tool: TaskTool,
        planner: RuleBasedPlanner | None = None,
    ):
        self.email_tool = email_tool
        self.task_tool = task_tool
        self.planner = planner or RuleBasedPlanner()

    def run(self, request: str) -> dict:
        plan = self.planner.plan(request)
        results = []

        for index, action in enumerate(plan, start=1):
            try:
                if action.tool == "email" and action.action == "draft":
                    result = self.email_tool.draft(**action.params)
                elif action.tool == "task" and action.action == "create":
                    result = self.task_tool.create(**action.params)
                else:
                    raise ValueError(f"Unsupported action: {action.tool}.{action.action}")

                results.append({
                    "step": index,
                    "status": "completed",
                    "tool": action.tool,
                    "action": action.action,
                    "result": result,
                })
            except Exception as exc:
                results.append({
                    "step": index,
                    "status": "failed",
                    "tool": action.tool,
                    "action": action.action,
                    "error": str(exc),
                })

        completed = sum(r["status"] == "completed" for r in results)
        failed = len(results) - completed

        return {
            "request": request,
            "plan": [
                {
                    "tool": a.tool,
                    "action": a.action,
                    "params": a.params,
                }
                for a in plan
            ],
            "summary": {
                "total_steps": len(results),
                "completed": completed,
                "failed": failed,
                "status": "completed" if failed == 0 else "partial_failure",
            },
            "results": results,
        }
