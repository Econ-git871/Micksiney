import unittest

from job_assistant.drafts import generate_draft, render_cover_letter, render_greeting
from job_assistant.models import Job, ResumeProfile


def _profile():
    return ResumeProfile(
        name="张三", titles=["咨询顾问"],
        skills=["python", "战略规划", "数据分析"],
        keywords=["python", "战略规划", "数据分析", "咨询顾问"],
        years_experience=5, education="硕士",
    )


def _job():
    return Job(title="战略咨询顾问", company="某咨询公司", location="上海",
               description="战略规划、行业研究、数据分析",
               matched=["战略规划", "数据分析", "咨询顾问"])


class DraftTests(unittest.TestCase):
    def test_greeting_mentions_role_and_company(self):
        text = render_greeting(_profile(), _job())
        self.assertIn("战略咨询顾问", text)
        self.assertIn("某咨询公司", text)
        self.assertIn("张三", text)

    def test_cover_letter_is_longer_and_named(self):
        text = render_cover_letter(_profile(), _job())
        self.assertGreater(len(text), len(render_greeting(_profile(), _job())))
        self.assertIn("张三", text)

    def test_generate_draft_dispatch(self):
        g = generate_draft(_profile(), _job(), style="greeting")
        c = generate_draft(_profile(), _job(), style="cover_letter")
        self.assertNotEqual(g, c)

    def test_invalid_style_raises(self):
        with self.assertRaises(ValueError):
            generate_draft(_profile(), _job(), style="nope")


if __name__ == "__main__":
    unittest.main()
