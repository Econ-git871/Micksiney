"""Core data structures shared across the package."""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Optional


def make_job_id(*parts: str) -> str:
    """Stable short id derived from identifying fields (url, or title+company)."""
    raw = "||".join(p.strip() for p in parts if p)
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:12]


@dataclass
class ResumeProfile:
    """Structured view of a resume, produced by :mod:`job_assistant.resume`."""

    name: str = ""
    titles: list[str] = field(default_factory=list)      # role keywords (顾问/分析师...)
    skills: list[str] = field(default_factory=list)      # matched hard skills
    keywords: list[str] = field(default_factory=list)    # union used for matching
    cities: list[str] = field(default_factory=list)      # locations, most frequent first
    years_experience: Optional[float] = None
    education: str = ""                                   # highest degree keyword
    summary: str = ""
    raw_text: str = ""

    def to_dict(self, include_raw: bool = False) -> dict:
        d = asdict(self)
        if not include_raw:
            d.pop("raw_text", None)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ResumeProfile":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class Job:
    """A single job posting from a provider."""

    id: str = ""
    title: str = ""
    company: str = ""
    location: str = ""
    description: str = ""
    url: str = ""
    source: str = ""        # platform name, e.g. BOSS直聘 / 智联招聘 / LinkedIn
    salary: str = ""
    posted: str = ""
    # populated by the matcher:
    score: float = 0.0
    matched: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id:
            self.id = make_job_id(self.url or "", self.title, self.company, self.source)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Job":
        known = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**known)


# Application status pipeline (求职进度).
STATUSES = [
    "matched",    # 已匹配
    "drafted",    # 已生成草稿
    "applied",    # 已投递
    "replied",    # HR 已回复
    "interview",  # 面试中
    "offer",      # 已发 offer
    "rejected",   # 未通过
    "closed",     # 已关闭/放弃
]

STATUS_ZH = {
    "matched": "已匹配",
    "drafted": "已生成草稿",
    "applied": "已投递",
    "replied": "HR已回复",
    "interview": "面试中",
    "offer": "已offer",
    "rejected": "未通过",
    "closed": "已关闭",
}
