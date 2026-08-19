from bs4 import BeautifulSoup
from datetime import datetime, timezone


class JobParser:

    def clean_description(self, html):
        if not html:
            return ""

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(" ", strip=True)

    def parse_job(self, job):
        min_salary = job.get("minSalary")
        max_salary = job.get("maxSalary")
        currency = job.get("currency")
        salary_period = job.get("salaryPeriod")

        salary = None

        if min_salary is not None and max_salary is not None:
            if min_salary == max_salary:
                salary = f"{currency} {min_salary:,} / {salary_period}"
            else:
                salary = (
                    f"{currency} {min_salary:,} - "
                    f"{max_salary:,} / {salary_period}"
                )

        pub_date = job.get("pubDate")

        published_at = None

        if pub_date:
            published_at = datetime.fromtimestamp(
                pub_date,
                tz=timezone.utc
            ).isoformat()

        return {
            "title": job.get("title", "").strip(),
            "company": job.get("companyName", "").strip(),
            "location": ", ".join(job.get("locationRestrictions", [])),
            "employment_type": job.get("employmentType"),
            "salary": salary,
            "seniority": ", ".join(job.get("seniority", [])),
            "description": self.clean_description(
                job.get("description", "")
            ),
            "url": job.get("applicationLink"),
            "source": "Himalayas",
            "published_at": published_at
        }