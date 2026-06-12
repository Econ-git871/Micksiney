"""Load jobs from a user-provided file (JSON or CSV).

This is the compliant way to bring in postings from any platform: export or
copy the listings you're interested in into a file, then let the tool rank them
and draft messages. Expected JSON shape: a list of objects, or an object with a
``"jobs"`` list. Recognized fields mirror :class:`job_assistant.models.Job`.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from ..models import Job, ResumeProfile
from .base import JobProvider


class FileProvider(JobProvider):
    name = "file"

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def fetch(self, profile: ResumeProfile | None = None) -> list[Job]:
        if not self.path.exists():
            raise FileNotFoundError(f"找不到岗位文件 / jobs file not found: {self.path}")
        suffix = self.path.suffix.lower()
        if suffix == ".json":
            return self._from_json()
        if suffix == ".csv":
            return self._from_csv()
        raise ValueError(f"不支持的岗位文件格式（支持 .json/.csv）：{suffix}")

    def _from_json(self) -> list[Job]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = data.get("jobs", [])
        return [Job.from_dict(item) for item in data]

    def _from_csv(self) -> list[Job]:
        with self.path.open(encoding="utf-8", newline="") as fh:
            return [Job.from_dict(row) for row in csv.DictReader(fh)]
