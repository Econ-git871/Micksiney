"""SQLite-backed application tracker (求职进度追踪)."""
from __future__ import annotations

import datetime
import sqlite3
from pathlib import Path

from .models import STATUSES, Job

_SCHEMA = """
CREATE TABLE IF NOT EXISTS applications(
    job_id       TEXT PRIMARY KEY,
    title        TEXT,
    company      TEXT,
    location     TEXT,
    source       TEXT,
    url          TEXT,
    score        REAL,
    status       TEXT,
    draft        TEXT,
    notes        TEXT,
    follow_up_on TEXT,
    created_at   TEXT,
    updated_at   TEXT
);
"""


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


class Tracker:
    """Thin wrapper over a SQLite table of applications."""

    def __init__(self, path: str | Path = "job_assistant.db") -> None:
        self.path = str(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(_SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "Tracker":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def upsert_jobs(self, jobs: list[Job], default_status: str = "matched") -> tuple[int, int]:
        """Insert new jobs / refresh existing ones. Returns (added, updated)."""
        now = _now()
        added = updated = 0
        for j in jobs:
            exists = self.conn.execute(
                "SELECT 1 FROM applications WHERE job_id=?", (j.id,)
            ).fetchone()
            if exists:
                self.conn.execute(
                    "UPDATE applications SET title=?,company=?,location=?,source=?,"
                    "url=?,score=?,updated_at=? WHERE job_id=?",
                    (j.title, j.company, j.location, j.source, j.url, j.score, now, j.id),
                )
                updated += 1
            else:
                self.conn.execute(
                    "INSERT INTO applications(job_id,title,company,location,source,url,"
                    "score,status,draft,notes,follow_up_on,created_at,updated_at) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (j.id, j.title, j.company, j.location, j.source, j.url, j.score,
                     default_status, "", "", None, now, now),
                )
                added += 1
        self.conn.commit()
        return added, updated

    def set_status(
        self,
        job_id: str,
        status: str | None = None,
        draft: str | None = None,
        notes: str | None = None,
        follow_up_on: str | None = None,
    ) -> bool:
        if status is not None and status not in STATUSES:
            raise ValueError(f"未知状态：{status}（可选：{', '.join(STATUSES)}）")
        fields, values = [], []
        for col, val in (
            ("status", status),
            ("draft", draft),
            ("notes", notes),
            ("follow_up_on", follow_up_on),
        ):
            if val is not None:
                fields.append(f"{col}=?")
                values.append(val)
        if not fields:
            return False
        fields.append("updated_at=?")
        values.append(_now())
        values.append(job_id)
        cur = self.conn.execute(
            f"UPDATE applications SET {', '.join(fields)} WHERE job_id=?", values
        )
        self.conn.commit()
        return cur.rowcount > 0

    def list(self, status: str | None = None) -> list[sqlite3.Row]:
        if status:
            rows = self.conn.execute(
                "SELECT * FROM applications WHERE status=? ORDER BY score DESC", (status,)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM applications ORDER BY score DESC"
            ).fetchall()
        return list(rows)

    def due_followups(self, on: str | None = None) -> list[sqlite3.Row]:
        on = on or datetime.date.today().isoformat()
        rows = self.conn.execute(
            "SELECT * FROM applications WHERE follow_up_on IS NOT NULL "
            "AND follow_up_on<=? ORDER BY follow_up_on", (on,)
        ).fetchall()
        return list(rows)

    def get(self, job_id: str) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM applications WHERE job_id=?", (job_id,)
        ).fetchone()
