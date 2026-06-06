"""Resume loading and parsing into a :class:`ResumeProfile`.

Native support: .txt / .md.  Optional: .pdf (needs ``pypdf``), .docx (needs
``python-docx``).  Parsing is heuristic and conservative — it never fabricates
fields it cannot find (e.g. years of experience is left as ``None``).
"""
from __future__ import annotations

import datetime
import re
from pathlib import Path

from . import lexicon
from .models import ResumeProfile

# Section headers we use to slice the document.
_WORK_HEADERS = ("工作经历", "工作经验", "项目经历", "Work Experience", "WORK EXPERIENCE", "Experience")
_EDU_HEADERS = ("教育经历", "教育背景", "Education", "EDUCATION")
_HIGHLIGHT_HEADERS = ("核心优势", "个人优势", "自我评价", "Summary", "SUMMARY", "About")

# Lines that look like section headers / common phrases — not names.
_HEADER_WORDS = {
    "核心优势", "工作经历", "工作经验", "教育经历", "教育背景", "项目经历", "其他",
    "技能", "证书", "执照", "语言", "项目成果", "承担工作", "关键产出", "产出成果",
    "联系方式", "个人信息", "自我评价", "求职意向", "专业技能",
}


def load_text(path: str | Path) -> str:
    """Read raw text from a resume file, dispatching on extension."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"找不到简历文件 / resume not found: {p}")
    suffix = p.suffix.lower()
    if suffix in {".txt", ".md", ".markdown", ""}:
        return p.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        return _load_pdf(p)
    if suffix == ".docx":
        return _load_docx(p)
    # Last resort: try to read as UTF-8 text.
    return p.read_text(encoding="utf-8", errors="ignore")


def _load_pdf(p: Path) -> str:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on env
        raise ModuleNotFoundError(
            "解析 PDF 需要 pypdf，请先安装： pip install pypdf"
        ) from exc
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:  # e.g. pyo3 PanicException from a broken native dep
        raise RuntimeError(
            f"pypdf 加载失败（运行环境的原生依赖问题）：{exc}。"
            "可改用 .txt/.md/.docx 简历，或修复 pypdf/cryptography 环境后重试。"
        ) from exc
    try:
        reader = PdfReader(str(p))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:
        raise RuntimeError(f"读取 PDF 失败：{exc}") from exc


def _load_docx(p: Path) -> str:
    try:
        import docx  # python-docx
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on env
        raise ModuleNotFoundError(
            "解析 Word 需要 python-docx，请先安装： pip install python-docx"
        ) from exc
    document = docx.Document(str(p))
    return "\n".join(par.text for par in document.paragraphs)


def _section(text: str, start_headers, end_headers) -> str:
    start = 0
    for kw in start_headers:
        i = text.find(kw)
        if i != -1:
            start = i
            break
    end = len(text)
    for kw in end_headers:
        j = text.find(kw, start + 1)
        if j != -1:
            end = min(end, j)
    return text[start:end]


def _estimate_years(text: str) -> float | None:
    """Estimate years of experience from year tokens in the work section."""
    work = _section(text, _WORK_HEADERS, _EDU_HEADERS)
    years = [int(y) for y in re.findall(r"(?:19|20)\d{2}", work)]
    if not years:
        return None
    span = datetime.date.today().year - min(years)
    return float(span) if 0 < span <= 50 else None


def _highest_degree(text: str) -> str:
    for deg in ("博士", "硕士", "本科", "学士", "MBA", "PhD", "Master", "Bachelor"):
        if deg in text:
            return deg
    return ""


def _summary(text: str) -> str:
    block = _section(text, _HIGHLIGHT_HEADERS, _WORK_HEADERS + _EDU_HEADERS)
    block = re.sub(r"\s+", " ", block).strip()
    if len(block) > 240:
        block = block[:240] + "…"
    return block


def _guess_name(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if not s or s in _HEADER_WORDS:
            continue
        # 2-4 CJK characters, standalone, not a known header/skill/role/city
        if re.fullmatch(r"[一-鿿]{2,4}", s):
            if s in _HEADER_WORDS or s in lexicon.SKILLS or s in lexicon.ROLES or s in lexicon.CITIES:
                continue
            return s
    return ""


def parse_resume(text: str, name: str | None = None) -> ResumeProfile:
    """Parse raw resume text into a structured :class:`ResumeProfile`."""
    profile = ResumeProfile(raw_text=text)
    profile.skills = lexicon.find_terms(text, lexicon.SKILLS)
    profile.titles = lexicon.find_terms(text, lexicon.ROLES)
    profile.cities = lexicon.find_terms(text, lexicon.CITIES, by_frequency=True)

    keywords: list[str] = []
    for term in profile.skills + profile.titles + lexicon.english_skills(text):
        if term not in keywords:
            keywords.append(term)
    profile.keywords = keywords

    profile.years_experience = _estimate_years(text)
    profile.education = _highest_degree(text)
    profile.summary = _summary(text)
    profile.name = name or _guess_name(text)
    return profile


def parse_file(path: str | Path, name: str | None = None) -> ResumeProfile:
    return parse_resume(load_text(path), name=name)
