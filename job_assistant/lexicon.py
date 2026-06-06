"""Bilingual (中文/English) term lexicon and lightweight tokenization.

We avoid heavyweight NLP deps (jieba / sklearn). Chinese terms are matched by
substring; ASCII terms are matched with word boundaries so short tokens like
``sql`` don't match inside larger words.
"""
from __future__ import annotations

import re
from collections import Counter

# --- Hard skills (mixed zh/en) -------------------------------------------------
SKILLS: list[str] = [
    # data / engineering
    "python", "sql", "excel", "vba", "powerpoint", "ppt", "word", "think-cell",
    "thinkcell", "tableau", "power bi", "powerbi", "spss", "sas", "stata",
    "pandas", "numpy", "matplotlib", "etl", "crawler", "web scraping", "scraping",
    "machine learning", "deep learning", "nlp", "statistics", "a/b testing",
    "financial modeling", "dcf", "data analysis", "data mining", "data visualization",
    "vibe coding",
    # data / engineering (中文)
    "数据分析", "数据清洗", "数据获取", "数据处理", "数据可视化", "数据挖掘",
    "爬虫", "网络爬虫", "建模", "统计分析", "商业分析", "财务建模", "财务分析",
    "营收测算", "可视化",
    # consulting / strategy (中文)
    "战略", "战略规划", "战略分析", "管理咨询", "咨询", "行业研究", "市场研究",
    "竞品分析", "竞争分析", "尽职调查", "投研", "标杆研究", "最佳实践",
    "商业计划书", "可行性研究", "政策研究", "产业规划", "专项规划", "区域经济",
    "国企改革", "机构改革", "组织架构", "组织优化", "流程优化", "岗位体系",
    "人力资源", "薪酬", "绩效", "薪酬绩效", "人才规划", "组织诊断",
    # certifications / methods
    "pmp", "cfa", "frm", "mba", "中级经济师", "issue-tree", "hypothesis-tree",
    "麦肯锡", "结构化思维",
]

# --- Role / title keywords -----------------------------------------------------
ROLES: list[str] = [
    "consultant", "analyst", "researcher", "strategy", "associate", "manager",
    "data analyst", "business analyst", "research analyst", "strategy analyst",
    "顾问", "咨询顾问", "资深顾问", "高级顾问", "战略顾问", "管理咨询顾问",
    "分析师", "研究员", "行业研究员", "数据分析师", "商业分析师", "战略分析师",
    "投资分析师", "咨询经理", "项目经理", "战略经理", "研究经理", "高级分析师",
    "战略规划", "投研分析师", "策略分析师",
]

# --- Cities (used for location matching) --------------------------------------
CITIES: list[str] = [
    "北京", "上海", "广州", "深圳", "武汉", "杭州", "成都", "南京", "重庆",
    "西安", "苏州", "天津", "长沙", "郑州", "青岛", "宁波", "东莞", "无锡",
    "厦门", "福州", "合肥", "济南", "大连", "沈阳", "哈尔滨", "昆明", "南昌",
    "海口", "三亚", "珠海", "佛山", "远程", "remote",
]

# English stopwords to drop during tokenization.
STOPWORDS_EN: set[str] = {
    "the", "and", "for", "with", "you", "our", "are", "will", "have", "has",
    "this", "that", "from", "your", "job", "work", "team", "role", "etc",
    "able", "who", "all", "any", "can", "use", "using", "into", "per",
}

_SKILLS_EN_LOWER = {t.lower() for t in SKILLS if t.isascii()}


def _is_ascii(term: str) -> bool:
    return term.isascii()


def term_in(term: str, text_lower: str) -> bool:
    """Whether ``term`` occurs in ``text_lower`` (already lower-cased)."""
    t = term.lower()
    if _is_ascii(t):
        if len(t) < 2:
            return False
        return re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", text_lower) is not None
    return t in text_lower


def find_terms(text: str, terms: list[str], by_frequency: bool = False) -> list[str]:
    """Return the subset of ``terms`` present in ``text`` (dedup, order-stable).

    When ``by_frequency`` is true, results are sorted by occurrence count desc.
    """
    low = text.lower()
    found: list[str] = []
    counts: Counter[str] = Counter()
    for term in terms:
        if _is_ascii(term) and len(term) < 2:
            continue
        if term_in(term, low):
            if term not in found:
                found.append(term)
            counts[term] = low.count(term.lower())
    if by_frequency:
        found.sort(key=lambda t: counts[t], reverse=True)
    return found


def tokenize_en(text: str) -> list[str]:
    """Extract distinct ASCII tokens (>=2 chars, non-stopword, non-numeric)."""
    tokens: list[str] = []
    seen: set[str] = set()
    for m in re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]{1,}", text.lower()):
        if m in STOPWORDS_EN or m.isdigit() or m in seen:
            continue
        seen.add(m)
        tokens.append(m)
    return tokens


def english_skills(text: str) -> list[str]:
    """ASCII skill tokens present in the text (subset of SKILLS)."""
    return [t for t in tokenize_en(text) if t in _SKILLS_EN_LOWER]
