# DECISIONS.md

## 1. Detection surface and ingestion strategy

Sites such as LinkedIn and Indeed can identify automated clients through browser/headless fingerprints, unusual request timing, missing or inconsistent headers, repeated requests, and abnormal browsing behaviour.

I deliberately did not bypass these protections. The assignment permits a low-risk public RSS/API source, so I used the public Himalayas job API as the primary source. This avoids authentication, browser automation, CAPTCHA bypassing, and protected user accounts.

The ingestion flow is:

Himalayas API → validation/retry → normalization → SQLite

If the API fails, is rate-limited, times out, or returns an invalid/empty response, the pipeline retries with exponential backoff and then switches to the public Himalayas RSS feed.

This was preferred over browser scraping because it is simpler, more reliable, and respects the scope guardrail while still demonstrating the ingestion and fallback pattern.

## 2. Resilience and fallback

The API fetcher handles timeouts, HTTP errors, and HTTP 429 rate limits with retries and exponential backoff. It also validates that the response contains a jobs collection and treats an empty response as a failure.

When the primary API cannot provide usable data, the RSS source is used as a fallback. Both sources are parsed into the same normalized job structure before being stored.

Jobs use their URL as a unique database key, preventing duplicate records when ingestion is run repeatedly.

If the primary source were permanently unavailable, I would add another independent public job-board RSS/API source rather than bypassing access controls.

## 3. Where I would stop

I would not bypass CAPTCHA, authentication, access controls, IP bans, or other technical restrictions. I would also avoid scraping a real user account or continuing against a source when its terms prohibit the activity.

For this demo, using a public API and RSS feed provides a lower-risk way to demonstrate the ingestion architecture without attempting to defeat anti-bot protections.

## 4. Trade-off under the time limit

I prioritized one reliable public source with an API/RSS fallback instead of implementing multiple job platforms or browser-based scraping.

With a full week, I would add more independent public sources, improve source-specific validation and monitoring, and add automated alerts when a source changes or repeatedly fails.

## 5. AI usage

I used AI assistance for code structure, debugging, and implementation suggestions. I personally ran and verified the fetchers, parsers, database operations, retry/fallback behaviour, duplicate handling, Flask dashboard, and deployment. I reviewed the final implementation so I can explain the decisions and code during the follow-up.