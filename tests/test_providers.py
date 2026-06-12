import io
import json
import unittest
from unittest import mock

from job_assistant.providers import AdzunaProvider, FileProvider, SampleProvider

SAMPLE_RESPONSE = {
    "results": [
        {
            "id": 12345,
            "title": "Strategy Consultant",
            "company": {"display_name": "ACME Consulting"},
            "location": {"display_name": "London, UK"},
            "description": "Strategy and data analysis for clients.",
            "redirect_url": "https://example.com/job/12345",
            "created": "2026-06-01T08:00:00Z",
            "salary_min": 50000,
            "salary_max": 70000,
        }
    ]
}


class _FakeResp(io.BytesIO):
    """A urlopen()-like object usable as a context manager."""

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


class SampleProviderTests(unittest.TestCase):
    def test_sample_loads(self):
        jobs = SampleProvider().fetch()
        self.assertTrue(jobs)
        self.assertTrue(all(j.title for j in jobs))


class AdzunaProviderTests(unittest.TestCase):
    def test_parses_response(self):
        provider = AdzunaProvider(country="gb", app_id="id", app_key="key")
        payload = json.dumps(SAMPLE_RESPONSE).encode("utf-8")
        with mock.patch("urllib.request.urlopen", return_value=_FakeResp(payload)):
            jobs = provider.fetch(query="strategy", where="London", results=5)
        self.assertEqual(len(jobs), 1)
        job = jobs[0]
        self.assertEqual(job.title, "Strategy Consultant")
        self.assertEqual(job.company, "ACME Consulting")
        self.assertEqual(job.source, "Adzuna")
        self.assertEqual(job.salary, "50000-70000")
        self.assertIn("London", job.location)

    def test_missing_credentials_raises(self):
        provider = AdzunaProvider(app_id=None, app_key=None)
        with self.assertRaises(RuntimeError):
            provider.fetch(query="x")


if __name__ == "__main__":
    unittest.main()
