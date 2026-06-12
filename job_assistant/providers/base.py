"""Provider interface."""
from __future__ import annotations

import abc

from ..models import Job, ResumeProfile


class JobProvider(abc.ABC):
    """A source of job postings.

    ``fetch`` may use the profile (e.g. to build a query for an official API),
    but implementations must respect the source's terms of service.
    """

    name: str = "provider"

    @abc.abstractmethod
    def fetch(self, profile: ResumeProfile | None = None) -> list[Job]:
        ...
