from bs4 import BeautifulSoup
from datetime import datetime


class RSSJobParser:

    def clean_description(self, html):
        if not html:
            return ""

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(" ", strip=True)

    def parse_job(self, entry):

        description = ""

        if hasattr(entry, "content") and entry.content:
            description = entry.content[0].get("value", "")

        published_at = None

        if getattr(entry, "published", None):
            try:
                published_at = datetime.strptime(
                    entry.published,
                    "%a, %d %b %Y %H:%M:%S %Z"
                ).isoformat()
            except ValueError:
                published_at = entry.published

        return {
            "title": entry.get("title", "").strip(),
            "company": entry.get(
                "himalayasjobs_companyname",
                ""
            ).strip(),
            "location": entry.get(
                "himalayasjobs_locationrestriction",
                ""
            ),
            "employment_type": None,
            "salary": None,
            "seniority": None,
            "description": self.clean_description(
                description
            ),
            "url": entry.get("link"),
            "source": "Himalayas RSS",
            "published_at": published_at
        }