import time
import requests


class HimalayasFetcher:
    API_URL = "https://himalayas.app/jobs/api"

    def fetch_jobs(self, limit=20, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    self.API_URL,
                    params={"limit": limit},
                    timeout=30
                )

                if response.status_code == 429:
                    wait_time = 2 ** attempt

                    print(
                        f"Rate limited. "
                        f"Waiting {wait_time} seconds before retry..."
                    )

                    time.sleep(wait_time)
                    continue

                response.raise_for_status()

                data = response.json()

                if "jobs" not in data:
                    raise ValueError(
                        "API response does not contain jobs"
                    )

                return data["jobs"]

            except requests.exceptions.Timeout:
                wait_time = 2 ** attempt

                print(
                    f"Request timed out. "
                    f"Waiting {wait_time} seconds before retry..."
                )

                time.sleep(wait_time)

            except requests.exceptions.RequestException as error:
                if attempt == max_retries - 1:
                    raise

                wait_time = 2 ** attempt

                print(
                    f"Request failed: {error}. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

        raise RuntimeError(
            "Himalayas API could not be reached after retries."
        )