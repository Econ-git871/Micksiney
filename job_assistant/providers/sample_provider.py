"""Bundled sample jobs, for the ``demo`` command and tests."""
from __future__ import annotations

import json
from importlib import resources

from ..models import Job, ResumeProfile
from .base import JobProvider


class SampleProvider(JobProvider):
    name = "sample"

    def fetch(self, profile: ResumeProfile | None = None) -> list[Job]:
        raw = resources.files("job_assistant.data").joinpath("sample_jobs.json").read_text(
            encoding="utf-8"
        )
        return [Job.from_dict(item) for item in json.loads(raw)]
