from app.fetchers.himalayas_fetcher import HimalayasFetcher
from app.parsers.job_parser import JobParser


fetcher = HimalayasFetcher()
parser = JobParser()

jobs = fetcher.fetch_jobs(limit=5)

print("Jobs fetched:", len(jobs))

print("\nNormalized jobs:\n")

for job in jobs:
    normalized_job = parser.parse_job(job)

    print("Title:", normalized_job["title"])
    print("Company:", normalized_job["company"])
    print("Location:", normalized_job["location"])
    print("Employment:", normalized_job["employment_type"])
    print("Salary:", normalized_job["salary"])
    print("Seniority:", normalized_job["seniority"])
    print("Source:", normalized_job["source"])
    print("URL:", normalized_job["url"])
    print("-" * 60)