"""Command-line interface.

辅助模式工作流：
    parse  解析简历 -> 画像
    match  对岗位打分排序（来自你导出的文件，或内置示例）
    draft  为某个岗位生成个性化草稿（模板，或 --llm 调用 Claude）
    track  记录/查看投递进度与跟进提醒
    demo   一键跑通内置示例（无需任何参数或依赖）

工具不会替你投递、也不会替你联系 HR——草稿请你审核后亲自发送。
"""
from __future__ import annotations

import argparse
import sys

from . import resume as resume_mod
from .drafts import STYLES, generate_draft
from .matching import score_jobs, top_matches
from .models import STATUS_ZH, ResumeProfile
from .providers import FileProvider, SampleProvider
from .storage import Tracker

DEFAULT_DB = "job_assistant.db"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _load_profile(args) -> ResumeProfile:
    try:
        profile = resume_mod.parse_file(args.resume, name=getattr(args, "name", None))
    except Exception as exc:  # CLI boundary: surface a friendly message, no traceback
        print(f"❌ 解析简历失败：{exc}", file=sys.stderr)
        raise SystemExit(2)
    if not profile.keywords:
        print("⚠️  未从简历中提取到技能关键词，匹配可能不准；可检查简历格式或内容。",
              file=sys.stderr)
    return profile


def _load_jobs(args, profile=None):
    if getattr(args, "sample", False):
        return SampleProvider().fetch()
    if getattr(args, "adzuna", False):
        from .providers import AdzunaProvider
        provider = AdzunaProvider(country=getattr(args, "country", None) or "gb")
        try:
            return provider.fetch(
                profile,
                query=getattr(args, "query", None),
                where=getattr(args, "where", None),
                results=getattr(args, "results", 20),
            )
        except RuntimeError as exc:
            print(f"❌ {exc}", file=sys.stderr)
            raise SystemExit(2)
    if getattr(args, "jobs", None):
        try:
            return FileProvider(args.jobs).fetch()
        except (FileNotFoundError, ValueError) as exc:
            print(f"❌ {exc}", file=sys.stderr)
            raise SystemExit(2)
    print("❌ 请用 --jobs <文件> 指定岗位文件、--sample 用内置示例，或 --adzuna 调官方API。",
          file=sys.stderr)
    raise SystemExit(2)


def _print_profile(p: ResumeProfile) -> None:
    print("=" * 60)
    print("📄 简历画像 / Resume profile")
    print("=" * 60)
    print(f"姓名     : {p.name or '（未识别，可用 --name 指定）'}")
    exp = f"约{int(p.years_experience)}年" if p.years_experience else "未识别"
    print(f"经验     : {exp}")
    print(f"学历     : {p.education or '未识别'}")
    print(f"地点     : {'、'.join(p.cities) or '未识别'}")
    print(f"方向     : {'、'.join(p.titles) or '未识别'}")
    print(f"技能     : {'、'.join(p.skills) or '未识别'}")
    if p.summary:
        print(f"自述     : {p.summary}")


def _print_jobs(jobs, limit: int | None = None) -> None:
    shown = jobs[:limit] if limit else jobs
    print("=" * 60)
    print(f"🎯 岗位匹配排序（共 {len(jobs)} 个，展示 {len(shown)} 个）")
    print("=" * 60)
    for i, j in enumerate(shown, 1):
        matched = "、".join(j.matched[:6]) if j.matched else "—"
        print(f"[{i}] 匹配度 {j.score:>5.1f}  {j.title} @ {j.company}")
        print(f"     地点:{j.location or '—'}  来源:{j.source or '—'}  "
              f"薪资:{j.salary or '—'}  id:{j.id}")
        print(f"     命中: {matched}")
        if j.url:
            print(f"     链接: {j.url}")
        print()


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
def cmd_parse(args) -> int:
    profile = _load_profile(args)
    if args.json:
        import json
        print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_profile(profile)
    return 0


def cmd_match(args) -> int:
    profile = _load_profile(args)
    jobs = _load_jobs(args, profile)
    ranked = top_matches(profile, jobs, limit=args.top, min_score=args.min_score)
    if not args.json:
        _print_profile(profile)
        print()
    if args.json:
        import json
        print(json.dumps([j.to_dict() for j in ranked], ensure_ascii=False, indent=2))
    else:
        _print_jobs(ranked)
    if args.save:
        with Tracker(args.db) as tracker:
            added, updated = tracker.upsert_jobs(ranked)
        print(f"💾 已写入追踪库 {args.db}：新增 {added}，更新 {updated}。"
              f"（用 `track list` 查看）")
    return 0


def cmd_draft(args) -> int:
    profile = _load_profile(args)
    jobs = _load_jobs(args, profile)
    ranked = score_jobs(profile, jobs)

    job = None
    if args.job_id:
        job = next((j for j in ranked if j.id == args.job_id), None)
        if job is None:
            print(f"❌ 未找到 id={args.job_id} 的岗位。", file=sys.stderr)
            return 2
    else:
        idx = max(1, args.rank) - 1
        if idx >= len(ranked):
            print(f"❌ 排名 {args.rank} 超出范围（共 {len(ranked)} 个岗位）。", file=sys.stderr)
            return 2
        job = ranked[idx]

    try:
        text = generate_draft(profile, job, style=args.style, use_llm=args.llm, model=args.model)
    except ModuleNotFoundError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 2

    style_zh = "打招呼语" if args.style == "greeting" else "求职信"
    print("=" * 60)
    print(f"✍️  {style_zh}草稿 — {job.title} @ {job.company}  (匹配度 {job.score})")
    print(f"    {'AI生成(Claude)' if args.llm else '模板生成'}；请审核后亲自发送")
    print("=" * 60)
    print(text)

    if args.save:
        with Tracker(args.db) as tracker:
            tracker.upsert_jobs([job])
            tracker.set_status(job.id, status="drafted", draft=text)
        print(f"\n💾 已保存草稿到追踪库 {args.db}（状态：已生成草稿）。")
    return 0


def cmd_track(args) -> int:
    with Tracker(args.db) as tracker:
        if args.action == "list":
            rows = tracker.list(status=args.status)
            if not rows:
                print("（追踪库为空。先运行 `match --save` 写入岗位。）")
                return 0
            print(f"📋 投递追踪（{len(rows)} 条）")
            print("-" * 60)
            for r in rows:
                st = STATUS_ZH.get(r["status"], r["status"])
                follow = f"  跟进:{r['follow_up_on']}" if r["follow_up_on"] else ""
                print(f"[{st}] {r['title']} @ {r['company']}  "
                      f"匹配度{r['score']}  id:{r['job_id']}{follow}")
                if r["notes"]:
                    print(f"    备注: {r['notes']}")
        elif args.action == "set":
            ok = tracker.set_status(
                args.job_id, status=args.status, notes=args.note, follow_up_on=args.follow
            )
            print("✅ 已更新。" if ok else "❌ 未找到该 id 或没有要更新的字段。")
            return 0 if ok else 2
        elif args.action == "due":
            rows = tracker.due_followups()
            if not rows:
                print("✅ 今天没有需要跟进的岗位。")
                return 0
            print(f"⏰ 待跟进（{len(rows)} 条）")
            for r in rows:
                print(f"  {r['follow_up_on']}  {r['title']} @ {r['company']}  id:{r['job_id']}")
    return 0


def cmd_demo(args) -> int:
    from importlib import resources
    print("▶ 运行内置示例（脱敏虚构数据，无需联网或 API Key）\n")
    resume_path = resources.files("job_assistant.data").joinpath("sample_resume.md")
    profile = resume_mod.parse_resume(resume_path.read_text(encoding="utf-8"))
    jobs = SampleProvider().fetch()
    ranked = top_matches(profile, jobs, limit=5)
    _print_profile(profile)
    print()
    _print_jobs(ranked)
    if ranked:
        print("—— 针对匹配度最高岗位生成的打招呼语草稿 ——")
        print(generate_draft(profile, ranked[0], style="greeting"))
    print("\n提示：用 `parse --resume 你的简历.pdf` 解析真实简历，"
          "再 `match --resume ... --jobs 岗位.json` 进行匹配。")
    return 0


# --------------------------------------------------------------------------- #
# argument parsing
# --------------------------------------------------------------------------- #
def _add_source_args(p: argparse.ArgumentParser) -> None:
    """Shared岗位来源参数：--jobs / --sample / --adzuna (+ adzuna 细项)。"""
    src = p.add_mutually_exclusive_group()
    src.add_argument("--jobs", help="岗位文件（.json/.csv，自行导出）")
    src.add_argument("--sample", action="store_true", help="使用内置示例岗位")
    src.add_argument("--adzuna", action="store_true",
                     help="从 Adzuna 官方API拉取（需 ADZUNA_APP_ID/ADZUNA_APP_KEY）")
    p.add_argument("--query", help="[adzuna] 搜索关键词（默认据简历自动生成英文关键词）")
    p.add_argument("--where", help="[adzuna] 地点（默认取简历城市）")
    p.add_argument("--country", default="gb",
                   help="[adzuna] 国家代码 gb/us/au/ca/de/fr/in/sg…（默认 gb；不含中国大陆）")
    p.add_argument("--results", type=int, default=20, help="[adzuna] 拉取条数（默认 20）")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="job-assistant",
        description="简历驱动的求职助手（辅助模式：搜索/匹配/草稿，投递由你亲自完成）",
    )
    parser.add_argument("--db", default=DEFAULT_DB, help=f"追踪库路径（默认 {DEFAULT_DB}）")
    sub = parser.add_subparsers(dest="command", required=True)

    # demo
    p_demo = sub.add_parser("demo", help="一键跑通内置示例")
    p_demo.set_defaults(func=cmd_demo)

    # parse
    p_parse = sub.add_parser("parse", help="解析简历为结构化画像")
    p_parse.add_argument("--resume", required=True, help="简历路径（.pdf/.docx/.txt/.md）")
    p_parse.add_argument("--name", help="手动指定姓名（解析不到时）")
    p_parse.add_argument("--json", action="store_true", help="以 JSON 输出")
    p_parse.set_defaults(func=cmd_parse)

    # match
    p_match = sub.add_parser("match", help="对岗位打分排序")
    p_match.add_argument("--resume", required=True, help="简历路径")
    p_match.add_argument("--name", help="手动指定姓名")
    _add_source_args(p_match)
    p_match.add_argument("--top", type=int, default=10, help="展示前 N 个（默认 10）")
    p_match.add_argument("--min-score", type=float, default=0.0, help="过滤低于该匹配度的岗位")
    p_match.add_argument("--save", action="store_true", help="写入追踪库")
    p_match.add_argument("--json", action="store_true", help="以 JSON 输出")
    p_match.set_defaults(func=cmd_match)

    # draft
    p_draft = sub.add_parser("draft", help="为某岗位生成个性化草稿")
    p_draft.add_argument("--resume", required=True, help="简历路径")
    p_draft.add_argument("--name", help="手动指定姓名")
    _add_source_args(p_draft)
    sel = p_draft.add_mutually_exclusive_group()
    sel.add_argument("--job-id", help="按岗位 id 选择")
    sel.add_argument("--rank", type=int, default=1, help="按匹配排名选择（默认 1=最高）")
    p_draft.add_argument("--style", choices=STYLES, default="greeting",
                         help="greeting=打招呼语，cover_letter=求职信")
    p_draft.add_argument("--llm", action="store_true",
                         help="调用 Claude 生成（需 anthropic 包与 ANTHROPIC_API_KEY）")
    p_draft.add_argument("--model", help="覆盖模型（默认 claude-opus-4-8）")
    p_draft.add_argument("--save", action="store_true", help="保存草稿到追踪库")
    p_draft.set_defaults(func=cmd_draft)

    # track
    p_track = sub.add_parser("track", help="投递进度追踪")
    tsub = p_track.add_subparsers(dest="action", required=True)
    t_list = tsub.add_parser("list", help="列出全部/按状态")
    t_list.add_argument("--status", help="按状态过滤")
    t_set = tsub.add_parser("set", help="更新某岗位状态/备注/跟进日期")
    t_set.add_argument("job_id")
    t_set.add_argument("--status", help="新状态")
    t_set.add_argument("--note", help="备注")
    t_set.add_argument("--follow", help="跟进日期 YYYY-MM-DD")
    t_due = tsub.add_parser("due", help="列出今天应跟进的岗位")
    p_track.set_defaults(func=cmd_track)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
