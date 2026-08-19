# Decisions

## 1. Why this ingestion strategy?

I chose a public Himalayas job API as the primary source because it provides structured job data without requiring browser automation or interacting with a protected user account.

The ingestion pipeline first requests jobs from the Himalayas API. If the primary request fails, the pipeline switches to the public Himalayas RSS feed. Both sources are converted into the same normalized job schema before being stored in SQLite.

I chose this approach instead of scraping sites such as LinkedIn or Indeed because the assignment specifically allows a low-risk public API/RSS source, and it demonstrates the same ingestion and fallback pattern without bypassing access controls.

## 2. Trade-off under the time limit

I prioritized reliability and a complete end-to-end ingestion pipeline over supporting multiple job platforms.

The current implementation uses one source with two ingestion paths: API and RSS fallback. With a full week, I would add more independent public sources, improve source-specific error handling, and add monitoring for changes in source responses.

## 3. AI usage

I used AI assistance while developing parts of the project, including code structure, debugging, and implementation suggestions.

I personally ran and verified the fetchers, parsers, database operations, fallback behavior, duplicate handling, Flask dashboard, and automated tests. I also reviewed the final code so I can explain the implementation and its decisions.