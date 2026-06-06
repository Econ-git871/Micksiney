# job-assistant · 简历驱动的求职助手

把求职里**重复、耗时**的部分自动化，把**关键动作**留给你本人——这是一个「辅助模式 / human-in-the-loop」的命令行工具：

1. **解析简历** → 结构化画像（技能 / 方向 / 经验 / 地点）
2. **匹配排序** → 根据你的简历给岗位打分，快速筛掉明显不合适的
3. **生成草稿** → 为每个岗位生成个性化的「打招呼语 / 求职信」草稿
4. **进度追踪** → 记录投了哪些、什么状态、何时跟进

> ✋ **它不会替你投递，也不会替你联系 HR。** 投递与沟通由你审核草稿后亲自完成。

## 为什么是「辅助」而不是「全自动」

全自动投递 + 自动私信 HR 看起来省事，但现实是：

- **违反平台规则**：BOSS直聘、智联招聘、前程无忧、LinkedIn、Indeed 等的用户协议都**明确禁止**脚本/爬虫/机器人自动投递与私信。
- **容易封号**：这些平台有验证码、设备指纹、行为风控，无人值守的自动化账号很容易被限制甚至封禁。
- **效果更差**：HR 能识别模板化/秒回的消息，海投也常被 ATS 直接过滤。**真正提升回复率的是「针对性」，不是「数量」。**

所以本工具刻意把"投递/私信"留给人——既合规，回复率也更高。岗位来源同样**不内置任何违规爬虫**：用[官方/授权 API]或你自己导出的岗位文件。

## 安装

核心功能**仅依赖 Python 标准库**（Python ≥ 3.10），不装任何第三方包也能跑：

```bash
python -m job_assistant demo          # 一键跑通内置示例（脱敏数据）
```

可选增强：

```bash
pip install -e .            # 安装为 `job-assistant` 命令
pip install -e .[all]       # 额外装 pypdf(读PDF) / python-docx(读Word) / anthropic(AI草稿)
# 或单独：pip install pypdf python-docx anthropic
```

## 快速开始

```bash
# 1) 解析你的简历（支持 .pdf/.docx/.txt/.md；读 PDF 需 pypdf）
python -m job_assistant parse --resume 我的简历.pdf

# 2) 准备岗位文件（见下方格式），匹配排序并写入追踪库
python -m job_assistant match --resume 我的简历.pdf --jobs jobs.json --top 10 --save

# 3) 为匹配度最高的岗位生成打招呼语草稿
python -m job_assistant draft --resume 我的简历.pdf --jobs jobs.json --rank 1 --style greeting

#    用 Claude 生成更个性化的版本（需 anthropic 包 + ANTHROPIC_API_KEY）
export ANTHROPIC_API_KEY=sk-ant-...
python -m job_assistant draft --resume 我的简历.pdf --jobs jobs.json --rank 1 --llm

# 4) 追踪进度
python -m job_assistant track list
python -m job_assistant track set <job_id> --status applied --follow 2026-06-20
python -m job_assistant track due
```

## 岗位文件格式

把你在各平台上看中的岗位**导出/整理**成一个 JSON（或 CSV），交给工具排序——这是合规引入岗位的方式。JSON 为对象数组：

```json
[
  {
    "title": "战略咨询顾问",
    "company": "某管理咨询公司",
    "location": "上海",
    "source": "BOSS直聘",
    "salary": "25-40K",
    "url": "https://...",
    "description": "战略规划、行业研究、商业计划书……"
  }
]
```

字段对应 `job_assistant/models.py` 里的 `Job`；`description` 越完整，匹配越准。可参考 `job_assistant/data/sample_jobs.json`。

## 匹配是怎么算的

透明、可解释（无黑盒向量）：对简历提取出的技能/方向关键词，与岗位文本做加权匹配——

- 命中**标题**的关键词额外加权；
- 用 IDF 降低"人人都写"的词的权重；
- 地点匹配加分；
- **中英同义词**：中文简历也能匹配英文岗位/JD（如 战略规划↔strategy planning、数据分析↔data analysis、行业研究↔industry research），词库见 `lexicon.py` 的 `SYNONYMS`；
- 最后归一化为 0–100 的**相对匹配度**（同一批里最契合的≈100）。

详见 `job_assistant/matching.py`。

## 接入更多岗位来源（合规）

实现 `job_assistant/providers/base.py` 里的 `JobProvider.fetch()` 即可，例如对接官方/授权 API。请遵守来源平台的服务条款——**不要**写违规爬虫。

## 隐私

- 简历含姓名/电话/邮箱等个人信息，**不要提交到仓库**。`.gitignore` 已默认排除 `*.pdf`、`*.docx`、`resumes/`、`private/`。
- 追踪库 `*.db` 也已被忽略。
- `--llm` 会把简历摘要与岗位信息发送给 Anthropic API；不需要时用默认的模板模式（完全本地）。

## 项目结构

```
job_assistant/
├── cli.py            # 命令行入口（parse/match/draft/track/demo）
├── resume.py         # 简历解析（pdf/docx/txt/md → ResumeProfile）
├── matching.py       # 岗位打分排序
├── drafts.py         # 草稿生成（模板 + 可选 Claude）
├── storage.py        # SQLite 进度追踪
├── lexicon.py        # 中英技能/角色/城市词库 + 分词
├── models.py         # ResumeProfile / Job / Application 等
├── providers/        # 岗位来源（示例 / 文件；可扩展授权API）
└── data/             # 脱敏示例简历与岗位
tests/                # 单元测试（python -m unittest）
```

## 测试

```bash
python -m unittest discover -s tests -v
```

## 许可

MIT
