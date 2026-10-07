from datetime import datetime, timezone
from pathlib import Path
import json


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


class TaskTool:
    """Creates local tasks/reminders; it never touches an external calendar."""

    def __init__(self, path: Path | None = None):
        self.path = path or DATA_DIR / "tasks.json"

    def create(self, title: str, due: str | None = None) -> dict:
        item = {
            "id": f"task-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            "title": title,
            "due": due,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "pending",
        }

        existing = self._read()
        existing.append(item)
        self.path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        return item

    def _read(self) -> list:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))
