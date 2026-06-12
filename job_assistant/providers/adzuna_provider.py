"""Adzuna provider — a working example of a compliant, official-API source.

Adzuna offers a free developer API (register at https://developer.adzuna.com)
covering many countries (gb / us / au / ca / de / fr / in / sg / ...). It does
**not** cover mainland China — for 国内 platforms there is no public job-search
API, so use the file/manual-import workflow instead.

Credentials come from env vars ``ADZUNA_APP_ID`` / ``ADZUNA_APP_KEY``.
Implemented with the standard library only (no extra dependencies).
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

from .. import lexicon
from ..models import Job, ResumeProfile
from .base import JobProvider


class AdzunaProvider(JobProvider):
    name = "adzuna"
    BASE = "https://api.adzuna.com/v1/api/jobs"

    def __init__(
        self,
        country: str = "gb",
        app_id: str | None = None,
        app_key: str | None = None,
        timeout: float = 15.0,
    ) -> None:
        self.country = country or "gb"
        self.app_id = app_id or os.getenv("ADZUNA_APP_ID")
        self.app_key = app_key or os.getenv("ADZUNA_APP_KEY")
        self.timeout = timeout

    def fetch(
        self,
        profile: ResumeProfile | None = None,
        query: str | None = None,
        where: str | None = None,
        results: int = 20,
        page: int = 1,
    ) -> list[Job]:
        if not self.app_id or not self.app_key:
            raise RuntimeError(
                "缺少 Adzuna 凭据：请在 https://developer.adzuna.com 免费注册，"
                "并设置环境变量 ADZUNA_APP_ID 与 ADZUNA_APP_KEY。"
            )
        what = query or self._default_what(profile)
        where = where if where is not None else self._default_where(profile)
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": max(1, min(results, 50)),
            "content-type": "application/json",
        }
        if what:
            params["what"] = what
        if where:
            params["where"] = where
        url = f"{self.BASE}/{self.country}/search/{page}?" + urllib.parse.urlencode(params)
        data = self._get_json(url)
        return [self._to_job(r) for r in data.get("results", [])]

    def _get_json(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": "job-assistant/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # network / HTTP / JSON errors
            raise RuntimeError(f"调用 Adzuna API 失败：{exc}") from exc

    @staticmethod
    def _default_what(profile: ResumeProfile | None) -> str:
        """Build an English keyword query from the (possibly Chinese) profile."""
        if not profile:
            return ""
        seeds = list(profile.titles[:1]) + list(profile.skills[:2])
        english = [lexicon.to_english(t) for t in seeds]
        # dedup, keep order
        return " ".join(dict.fromkeys(t for t in english if t))

    @staticmethod
    def _default_where(profile: ResumeProfile | None) -> str:
        if profile and profile.cities:
            return lexicon.to_english(profile.cities[0])
        return ""

    @staticmethod
    def _to_job(r: dict) -> Job:
        loc = r.get("location") or {}
        comp = r.get("company") or {}
        salary = ""
        smin, smax = r.get("salary_min"), r.get("salary_max")
        if smin or smax:
            salary = f"{int(smin or 0)}-{int(smax or 0)}"
        return Job(
            id=str(r.get("id", "")),
            title=(r.get("title") or "").strip(),
            company=(comp.get("display_name", "") if isinstance(comp, dict) else "").strip(),
            location=(loc.get("display_name", "") if isinstance(loc, dict) else "").strip(),
            description=(r.get("description") or "").strip(),
            url=r.get("redirect_url", ""),
            source="Adzuna",
            salary=salary,
            posted=(r.get("created") or "")[:10],
        )
