import unittest

from app.fetchers.himalayas_fetcher import HimalayasFetcher
from app.fetchers.himalayas_rss_fetcher import HimalayasRSSFetcher

from app.parsers.job_parser import JobParser
from app.parsers.rss_job_parser import RSSJobParser


class TestPipeline(unittest.TestCase):

    def test_api_fetcher(self):
        fetcher = HimalayasFetcher()

        jobs = fetcher.fetch_jobs(limit=5)

        self.assertGreater(len(jobs), 0)

    def test_api_parser(self):
        fetcher = HimalayasFetcher()
        parser = JobParser()

        jobs = fetcher.fetch_jobs(limit=1)

        job = parser.parse_job(jobs[0])

        self.assertIn("title", job)
        self.assertIn("company", job)
        self.assertIn("url", job)
        self.assertEqual(job["source"], "Himalayas")

    def test_rss_fetcher(self):
        fetcher = HimalayasRSSFetcher()

        jobs = fetcher.fetch_jobs()

        self.assertGreater(len(jobs), 0)

    def test_rss_parser(self):
        fetcher = HimalayasRSSFetcher()
        parser = RSSJobParser()

        jobs = fetcher.fetch_jobs()

        job = parser.parse_job(jobs[0])

        self.assertIn("title", job)
        self.assertIn("company", job)
        self.assertIn("url", job)
        self.assertEqual(job["source"], "Himalayas RSS")


if __name__ == "__main__":
    unittest.main()