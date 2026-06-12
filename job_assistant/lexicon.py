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


# --- Cross-language synonyms (中↔英) ------------------------------------------
# Each inner list groups equivalent surface forms across Chinese and English so
# a Chinese resume can match an English job description (and vice versa).
SYNONYMS: list[list[str]] = [
    ["战略", "strategy", "strategic"],
    ["战略规划", "strategy planning", "strategic planning"],
    ["战略分析", "strategy analysis", "strategic analysis"],
    ["管理咨询", "咨询", "consulting", "management consulting"],
    ["顾问", "consultant"],
    ["分析师", "analyst"],
    ["研究员", "researcher", "research analyst"],
    ["行业研究", "industry research"],
    ["市场研究", "market research"],
    ["竞品分析", "竞争分析", "competitive analysis", "competitor analysis"],
    ["尽职调查", "due diligence"],
    ["数据分析", "data analysis", "data analytics"],
    ["数据清洗", "data cleaning", "data cleansing"],
    ["数据获取", "data collection"],
    ["数据可视化", "可视化", "data visualization"],
    ["数据挖掘", "data mining"],
    ["爬虫", "网络爬虫", "crawler", "web scraping", "scraping"],
    ["建模", "modeling", "modelling"],
    ["财务建模", "financial modeling"],
    ["财务分析", "financial analysis"],
    ["商业分析", "business analysis"],
    ["商业计划书", "business plan"],
    ["可行性研究", "feasibility study"],
    ["机器学习", "machine learning"],
    ["统计分析", "statistics", "statistical analysis"],
    ["项目管理", "project management"],
    ["组织架构", "组织优化", "organization design", "organizational design", "org design"],
    ["组织诊断", "organizational diagnosis"],
    ["岗位体系", "job architecture", "job grading"],
    ["薪酬", "compensation"],
    ["绩效", "performance management"],
    ["薪酬绩效", "compensation and benefits", "comp & ben"],
    ["人才规划", "talent planning", "workforce planning"],
    ["机构改革", "restructuring", "reorganization"],
    ["结构化思维", "structured thinking"],
    ["产业规划", "industrial planning"],
]


def _build_concepts(groups: list[list[str]]) -> dict[str, frozenset[str]]:
    index: dict[str, frozenset[str]] = {}
    for group in groups:
        forms = frozenset(g.lower() for g in group)
        for form in group:
            index[form.lower()] = forms
    return index


_CONCEPTS = _build_concepts(SYNONYMS)


def concept_forms(term: str) -> frozenset[str]:
    """All equivalent surface forms of ``term`` (itself if it has no group)."""
    return _CONCEPTS.get(term.lower(), frozenset({term.lower()}))


def concept_match(term: str, text_lower: str) -> bool:
    """Whether ``term`` — or any cross-language synonym — occurs in the text."""
    return any(term_in(form, text_lower) for form in concept_forms(term))


def to_english(term: str) -> str:
    """Return an ASCII (English) synonym of ``term`` if one exists, else ``term``.

    Used to turn Chinese resume keywords into a query for English job APIs.
    """
    for form in sorted(concept_forms(term)):
        if form.isascii():
            return form
    return term

