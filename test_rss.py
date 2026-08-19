from app.fetchers.himalayas_rss_fetcher import HimalayasRSSFetcher
from app.parsers.rss_job_parser import RSSJobParser


fetcher = HimalayasRSSFetcher()
parser = RSSJobParser()

jobs = fetcher.fetch_jobs()

print("RSS jobs fetched:", len(jobs))

job = parser.parse_job(jobs[0])

print("\nNormalized RSS job:")
print("Title:", job["title"])
print("Company:", job["company"])
print("Location:", job["location"])
print("Source:", job["source"])
print("URL:", job["url"])
print("Published:", job["published_at"])
print("Description:", job["description"][:200])