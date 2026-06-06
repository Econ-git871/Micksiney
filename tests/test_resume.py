import unittest

from job_assistant.resume import parse_resume

SAMPLE = """张三
138-0000-0000 | zhangsan@example.com | 武汉

核心优势
数据分析：精通 Python、SQL，擅长爬虫与数据清洗

工作经历
某咨询公司  2021年06月 - 至今  咨询顾问  武汉
主导战略规划与行业研究项目

教育经历
武汉大学  管理科学 硕士 2024年09月 - 2026年06月
"""


class ParseResumeTests(unittest.TestCase):
    def test_extracts_skills(self):
        p = parse_resume(SAMPLE)
        self.assertIn("python", [s.lower() for s in p.skills])
        self.assertIn("sql", [s.lower() for s in p.skills])
        self.assertIn("战略规划", p.skills)

    def test_extracts_roles_and_city(self):
        p = parse_resume(SAMPLE)
        self.assertIn("咨询顾问", p.titles)
        self.assertIn("武汉", p.cities)

    def test_estimates_experience_from_work_section(self):
        p = parse_resume(SAMPLE)
        # work started 2021; education years (2024/2026) must be excluded
        self.assertIsNotNone(p.years_experience)
        self.assertGreaterEqual(p.years_experience, 4)

    def test_name_override(self):
        p = parse_resume(SAMPLE, name="李四")
        self.assertEqual(p.name, "李四")

    def test_highest_degree(self):
        p = parse_resume(SAMPLE)
        self.assertEqual(p.education, "硕士")


if __name__ == "__main__":
    unittest.main()
