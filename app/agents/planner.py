from dataclasses import dataclass
import re


@dataclass
class PlannedAction:
    tool: str
    action: str
    params: dict


class RuleBasedPlanner:
    """
    Zero-API-key planner.

    It intentionally favors predictable actions over free-form generation.
    An LLM planner can later implement the same plan(request) interface.
    """

    def plan(self, request: str) -> list[PlannedAction]:
        text = request.strip()
        lower = text.lower()
        actions: list[PlannedAction] = []

        email_requested = any(
            word in lower for word in [
                "email", "mail", "draft", "write an email", "send an email"
            ]
        )
        task_requested = any(
            word in lower for word in [
                "remind", "reminder", "task", "todo", "to-do", "follow up"
            ]
        )

        if email_requested:
            recipient = self._extract_recipient(text)
            subject = self._subject_from_request(text)
            body = self._draft_body(text)
            actions.append(
                PlannedAction(
                    tool="email",
                    action="draft",
                    params={"to": recipient, "subject": subject, "body": body},
                )
            )

        if task_requested:
            due = self._extract_due(text)
            title = self._task_title(text)
            actions.append(
                PlannedAction(
                    tool="task",
                    action="create",
                    params={"title": title, "due": due},
                )
            )

        if not actions:
            actions.append(
                PlannedAction(
                    tool="task",
                    action="create",
                    params={
                        "title": f"Review request: {text[:80]}",
                        "due": None,
                    },
                )
            )

        return actions

    @staticmethod
    def _extract_recipient(text: str) -> str:
        match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)
        if match:
            return match.group(0)
        return "draft-recipient@example.com"

    @staticmethod
    def _subject_from_request(text: str) -> str:
        lower = text.lower()
        if "interview" in lower:
            return "Interview Follow-up"
        if "meeting" in lower:
            return "Meeting Follow-up"
        if "application" in lower or "job" in lower:
            return "Application Follow-up"
        return "Work Follow-up"

    @staticmethod
    def _draft_body(text: str) -> str:
        return (
            "Hi,\n\n"
            "I’m following up regarding the request below:\n\n"
            f"{text}\n\n"
            "Please let me know if there are any updates or next steps.\n\n"
            "Best regards,\n"
            "Farhan"
        )

    @staticmethod
    def _extract_due(text: str) -> str | None:
        lower = text.lower()
        for phrase in [
            "tomorrow at 10 am",
            "tomorrow at 9 am",
            "tomorrow",
            "today",
            "next week",
        ]:
            if phrase in lower:
                return phrase
        return None

    @staticmethod
    def _task_title(text: str) -> str:
        lower = text.lower()
        if "interview" in lower:
            return "Send interview follow-up"
        if "meeting" in lower:
            return "Follow up on meeting"
        if "application" in lower or "job" in lower:
            return "Follow up on job application"
        return "Complete requested follow-up"
