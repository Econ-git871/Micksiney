import os
import tempfile
import unittest

from job_assistant.models import Job
from job_assistant.storage import Tracker


class StorageTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".db")
        os.close(fd)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_upsert_and_list(self):
        with Tracker(self.path) as t:
            jobs = [Job(title="数据分析师", company="A"), Job(title="顾问", company="B")]
            added, updated = t.upsert_jobs(jobs)
            self.assertEqual((added, updated), (2, 0))
            # re-upsert updates, not duplicates
            added2, updated2 = t.upsert_jobs(jobs)
            self.assertEqual((added2, updated2), (0, 2))
            self.assertEqual(len(t.list()), 2)

    def test_status_roundtrip(self):
        with Tracker(self.path) as t:
            job = Job(title="顾问", company="B")
            t.upsert_jobs([job])
            self.assertTrue(t.set_status(job.id, status="applied", notes="已投"))
            row = t.get(job.id)
            self.assertEqual(row["status"], "applied")
            self.assertEqual(row["notes"], "已投")

    def test_invalid_status_raises(self):
        with Tracker(self.path) as t:
            job = Job(title="顾问", company="B")
            t.upsert_jobs([job])
            with self.assertRaises(ValueError):
                t.set_status(job.id, status="not-a-status")

    def test_due_followups(self):
        with Tracker(self.path) as t:
            job = Job(title="顾问", company="B")
            t.upsert_jobs([job])
            t.set_status(job.id, follow_up_on="2000-01-01")  # past date => due
            self.assertEqual(len(t.due_followups()), 1)


if __name__ == "__main__":
    unittest.main()
