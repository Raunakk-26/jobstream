from flask import Flask, render_template, request

from app.database.database import (
    get_connection,
    get_latest_ingestion
)


app = Flask(__name__)


# ============================================================
# HOME / DASHBOARD
# ============================================================

@app.route("/")
def home():

    connection = get_connection()

    # --------------------------------------------------------
    # GET LATEST JOBS
    # --------------------------------------------------------

    jobs = connection.execute("""
        SELECT
            id,
            title,
            company,
            location,
            employment_type,
            salary,
            seniority,
            description,
            url,
            source,
            published_at,
            created_at
        FROM jobs
        ORDER BY created_at DESC
        LIMIT 50
    """).fetchall()

    connection.close()

    # --------------------------------------------------------
    # GET LAST INGESTION REPORT
    # --------------------------------------------------------

    ingestion = get_latest_ingestion()

    # --------------------------------------------------------
    # RENDER DASHBOARD
    # --------------------------------------------------------

    return render_template(
        "index.html",
        jobs=jobs,
        ingestion=ingestion
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run()