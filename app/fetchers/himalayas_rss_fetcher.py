import feedparser
import requests


class HimalayasRSSFetcher:
    RSS_URL = "https://himalayas.app/jobs/rss"

    def fetch_jobs(self):
        response = requests.get(
            self.RSS_URL,
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"RSS request failed with status {response.status_code}"
            )

        feed = feedparser.parse(response.content)

        if not feed.entries:
            raise ValueError("RSS feed returned no jobs")

        return feed.entries