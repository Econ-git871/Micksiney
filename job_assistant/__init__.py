"""job_assistant — 简历驱动的求职助手 (resume-driven job-search assistant).

辅助模式（human-in-the-loop）：工具负责
  1) 解析简历 -> 结构化画像
  2) 对岗位打分排序，过滤明显不合适的
  3) 生成个性化的打招呼语 / 求职信草稿
最终的「投递」与「联系 HR」由你本人审核后亲自完成——
既符合各招聘平台的规则，回复率也更高。
"""
from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]
