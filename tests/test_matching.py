import unittest

from job_assistant.matching import score_jobs, top_matches
from job_assistant.models import Job, ResumeProfile


def _profile():
    return ResumeProfile(
        name="测试",
        titles=["咨询顾问", "分析师"],
        skills=["python", "sql", "战略规划", "行业研究", "数据分析"],
        keywords=["python", "sql", "战略规划", "行业研究", "数据分析", "咨询顾问", "分析师"],
        cities=["武汉"],
    )


def _jobs():
    return [
        Job(title="战略咨询顾问", company="某咨询", location="上海",
            description="战略规划、行业研究、商业计划书"),
        Job(title="数据分析师", company="某互联网", location="武汉",
            description="SQL、Python、数据清洗、数据分析"),
        Job(title="前端开发工程师", company="某科技", location="杭州",
            description="React、Vue、JavaScript、CSS 前端开发"),
    ]


class MatchingTests(unittest.TestCase):
    def test_relevant_ranks_above_irrelevant(self):
        ranked = score_jobs(_profile(), _jobs())
        titles = [j.title for j in ranked]
        self.assertEqual(titles[-1], "前端开发工程师")  # control job last
        self.assertIn(ranked[0].title, {"战略咨询顾问", "数据分析师"})

    def test_top_score_normalized_to_100(self):
        ranked = score_jobs(_profile(), _jobs())
        self.assertEqual(ranked[0].score, 100.0)

    def test_matched_terms_recorded(self):
        ranked = score_jobs(_profile(), _jobs())
        consulting = next(j for j in ranked if j.title == "战略咨询顾问")
        self.assertIn("战略规划", consulting.matched)

    def test_min_score_filter(self):
        kept = top_matches(_profile(), _jobs(), min_score=50.0)
        self.assertTrue(all(j.score >= 50.0 for j in kept))

    def test_empty_jobs(self):
        self.assertEqual(score_jobs(_profile(), []), [])


if __name__ == "__main__":
    unittest.main()
