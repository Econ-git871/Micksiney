"""Generate personalized outreach drafts.

Default: dependency-free template (works offline).
Optional: Claude API for a more tailored draft when ``use_llm=True`` and the
``anthropic`` package + ``ANTHROPIC_API_KEY`` are available.

These are *drafts* — you review and send them yourself. The tool never contacts
HR or submits applications on your behalf.
"""
from __future__ import annotations

import os

from . import lexicon
from .models import Job, ResumeProfile

# Default model. Override with env JOB_ASSISTANT_MODEL.
DEFAULT_MODEL = "claude-opus-4-8"

STYLES = ("greeting", "cover_letter")


def _top_skills(profile: ResumeProfile, job: Job, n: int = 3) -> list[str]:
    """Skills that both the resume and this job share (fallback: top resume skills)."""
    shared = [s for s in (job.matched or []) if s in profile.skills]
    if not shared:
        shared = [s for s in profile.skills if lexicon.term_in(s, job.description.lower())]
    if not shared:
        shared = list(profile.skills)
    # prefer readable Chinese terms first
    shared.sort(key=lambda s: 0 if not s.isascii() else 1)
    out: list[str] = []
    for s in shared:
        if s not in out:
            out.append(s)
        if len(out) >= n:
            break
    return out


def _exp_phrase(profile: ResumeProfile) -> str:
    if profile.years_experience and profile.years_experience >= 1:
        return f"{int(profile.years_experience)}年"
    return ""


def render_greeting(profile: ResumeProfile, job: Job) -> str:
    """Short, BOSS直聘-style opener (review before sending)."""
    who = profile.name or "您好"
    exp = _exp_phrase(profile)
    skills = "、".join(_top_skills(profile, job)) or "相关"
    role_kw = profile.titles[0] if profile.titles else "相关"
    company = job.company or "贵公司"

    lead = f"您好！我是{profile.name}，" if profile.name else "您好！"
    bg = f"有{exp}{role_kw}经验" if exp else f"有{role_kw}相关经验"
    return (
        f"{lead}关注到{company}的「{job.title}」岗位，很感兴趣。"
        f"我{bg}，擅长{skills}；"
        f"与岗位要求比较契合，希望能进一步沟通，期待您的回复，谢谢！"
    )


def render_cover_letter(profile: ResumeProfile, job: Job) -> str:
    """Longer cover letter (review before sending)."""
    exp = _exp_phrase(profile)
    skills = "、".join(_top_skills(profile, job, n=4)) or "相关技能"
    company = job.company or "贵公司"
    name = profile.name or "（你的姓名）"
    edu = f"，{profile.education}学历" if profile.education else ""

    intro = (
        f"尊敬的招聘负责人：\n\n"
        f"您好！我是{name}{edu}。看到{company}正在招聘「{job.title}」，"
        f"在了解岗位职责后，我认为自身经历与该职位高度匹配，特此应聘。\n\n"
    )
    body = (
        f"我{('拥有' + exp) if exp else '具备相关的'}从业经验，核心能力包括 {skills}。"
        f"在过往工作中，我能够独立完成从需求分析、数据获取到结论交付的端到端工作，"
        f"并擅长用结构化思维拆解复杂问题、形成可落地的方案。\n\n"
    )
    closing = (
        f"我对{company}的业务方向很认同，相信能在「{job.title}」岗位上创造价值。"
        f"期待有机会进一步沟通，感谢您的时间！\n\n"
        f"此致\n敬礼\n{name}"
    )
    return intro + body + closing


def _profile_brief(profile: ResumeProfile) -> str:
    parts = []
    if profile.name:
        parts.append(f"姓名：{profile.name}")
    if profile.years_experience:
        parts.append(f"经验：约{int(profile.years_experience)}年")
    if profile.education:
        parts.append(f"学历：{profile.education}")
    if profile.titles:
        parts.append("方向：" + "、".join(profile.titles[:4]))
    if profile.skills:
        parts.append("技能：" + "、".join(profile.skills[:10]))
    if profile.summary:
        parts.append("自述：" + profile.summary)
    return "\n".join(parts)


def _llm_draft(profile: ResumeProfile, job: Job, style: str, model: str | None) -> str:
    """Tailored draft via the Anthropic SDK. Raises if unavailable."""
    try:
        import anthropic
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "使用 --llm 需要 anthropic 包： pip install anthropic，并设置 ANTHROPIC_API_KEY"
        ) from exc

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    kind = (
        "一段主动打招呼语（150字以内，适合在 BOSS直聘等平台首次联系 HR）"
        if style == "greeting"
        else "一封求职信（300-400字，可用于邮件或平台附言）"
    )
    system = (
        "你是一名资深职业顾问，帮助求职者撰写个性化、真诚、简洁的求职沟通内容。"
        "只能依据提供的简历信息，绝不编造未提及的经历或数字；语气专业不浮夸；中文输出，只返回正文。"
    )
    user = (
        f"请根据以下信息，写{kind}：\n\n"
        f"【简历信息】\n{_profile_brief(profile)}\n\n"
        f"【目标岗位】\n岗位：{job.title}\n公司：{job.company}\n"
        f"地点：{job.location}\n来源：{job.source}\n职位描述：{job.description}\n\n"
        f"要求：突出与该岗位最相关的 2-3 个匹配点，结尾给出明确的沟通意向。"
    )
    resp = client.messages.create(
        model=model or os.getenv("JOB_ASSISTANT_MODEL", DEFAULT_MODEL),
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def generate_draft(
    profile: ResumeProfile,
    job: Job,
    style: str = "greeting",
    use_llm: bool = False,
    model: str | None = None,
) -> str:
    """Generate a draft. Falls back to templates if the LLM path is unavailable."""
    if style not in STYLES:
        raise ValueError(f"style 必须是 {STYLES} 之一，收到：{style}")
    if use_llm:
        return _llm_draft(profile, job, style, model)
    return render_greeting(profile, job) if style == "greeting" else render_cover_letter(profile, job)
