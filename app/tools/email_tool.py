from datetime import datetime, timezone
from pathlib import Path
import json


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


class EmailTool:
    """Creates local email drafts; it never sends mail."""

    def __init__(self, path: Path | None = None):
        self.path = path or DATA_DIR / "email_drafts.json"

    def draft(self, to: str, subject: str, body: str) -> dict:
        item = {
            "id": f"draft-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            "to": to,
            "subject": subject,
            "body": body,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "draft",
        }

        existing = self._read()
        existing.append(item)
        self.path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        return item

    def _read(self) -> list:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))
