"""Job providers — pluggable sources of job postings.

Design note (合规说明): providers are deliberately limited to sources that do
NOT violate platform terms of service:
  * SampleProvider  — bundled demo data
  * FileProvider    — jobs you exported yourself (JSON / CSV)

Platform-specific scrapers are intentionally NOT bundled. Major job boards
(BOSS直聘 / 智联招聘 / 前程无忧 / LinkedIn / Indeed) prohibit automated scraping
and bot messaging in their user agreements. To add a compliant source, implement
the :class:`JobProvider` interface against an official/authorized API.
"""
from __future__ import annotations

from .base import JobProvider
from .file_provider import FileProvider
from .sample_provider import SampleProvider

__all__ = ["JobProvider", "FileProvider", "SampleProvider"]
