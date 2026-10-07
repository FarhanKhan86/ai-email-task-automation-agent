from app.agents.planner import RuleBasedPlanner


def test_email_and_reminder_plan():
    actions = RuleBasedPlanner().plan(
        "Draft an email to Sarah at sarah@example.com about my interview and remind me tomorrow."
    )

    assert len(actions) == 2
    assert actions[0].tool == "email"
    assert actions[0].action == "draft"
    assert actions[0].params["to"] == "sarah@example.com"
    assert actions[1].tool == "task"
    assert actions[1].params["due"] == "tomorrow"


def test_fallback_creates_task():
    actions = RuleBasedPlanner().plan("Prepare my project notes")
    assert len(actions) == 1
    assert actions[0].tool == "task"
