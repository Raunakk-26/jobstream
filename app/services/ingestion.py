from app.database.database import (
    create_jobs_table,
    save_job,
    save_ingestion_report
)

from app.fetchers.himalayas_fetcher import HimalayasFetcher
from app.fetchers.himalayas_rss_fetcher import HimalayasRSSFetcher

from app.parsers.job_parser import JobParser
from app.parsers.rss_job_parser import RSSJobParser


def run_ingestion():

    # Create database tables if they do not exist
    create_jobs_table()

    source = "Himalayas API"
    fallback_used = False
    error = None

    fetched_jobs = []

    # ---------------------------------------------------------
    # PRIMARY SOURCE: HIMALAYAS API
    # ---------------------------------------------------------

    try:

        fetcher = HimalayasFetcher()

        fetched_jobs = fetcher.fetch_jobs(
            limit=20
        )

    except Exception as api_error:

        print(
            f"API failed: {api_error}"
        )

        # -----------------------------------------------------
        # FALLBACK: HIMALAYAS RSS
        # -----------------------------------------------------

        try:

            fallback_used = True
            source = "Himalayas RSS"

            rss_fetcher = HimalayasRSSFetcher()

            fetched_jobs = rss_fetcher.fetch_jobs()

        except Exception as rss_error:

            error = str(rss_error)

            print(
                f"RSS fallback failed: {rss_error}"
            )

            fetched_jobs = []


    # ---------------------------------------------------------
    # PARSE JOBS
    # ---------------------------------------------------------

    if fallback_used:

        parser = RSSJobParser()

    else:

        parser = JobParser()


    new_jobs = 0
    duplicates = 0


    # ---------------------------------------------------------
    # SAVE JOBS
    # ---------------------------------------------------------

    for raw_job in fetched_jobs:

        try:

            job = parser.parse_job(
                raw_job
            )

            inserted = save_job(
                job
            )

            if inserted:

                new_jobs += 1

            else:

                duplicates += 1

        except Exception as parse_error:

            print(
                f"Could not process job: {parse_error}"
            )


    # ---------------------------------------------------------
    # SAVE INGESTION REPORT
    # ---------------------------------------------------------

    report = {

        "source": source,

        "fetched": len(fetched_jobs),

        "new_jobs": new_jobs,

        "duplicates": duplicates,

        "fallback_used": fallback_used,

        "error": error
    }


    save_ingestion_report(
        report
    )


    # ---------------------------------------------------------
    # PRINT REPORT
    # ---------------------------------------------------------

    print()
    print("========== INGESTION REPORT ==========")
    print(f"Source:       {source}")
    print(f"Fetched:      {len(fetched_jobs)}")
    print(f"New jobs:     {new_jobs}")
    print(f"Duplicates:   {duplicates}")
    print(f"Fallback:     {fallback_used}")
    print("======================================")
    print()


    return report


if __name__ == "__main__":

    run_ingestion()