from firecrawl import FirecrawlApp
from config import FIRECRAWL_API_KEY, COMPETITORS
from storage.db import get_last_snapshot, save_snapshot

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def collect_jobs_signals():
    all_signals = []

    for competitor in COMPETITORS:
        comp_name = competitor.get("name")
        jobs_url = competitor.get("jobs_url")

        if not jobs_url:
            continue

        print(f"Collecting jobs for {comp_name}...")

        try:
            result = app.scrape_url(jobs_url, formats=["markdown"])
            current_jobs = result.markdown or ""

            last = get_last_snapshot("jobs_snapshots", comp_name)
            changes = []

            if last:
                if last[2] != current_jobs:
                    changes.append("Job postings have changed")
                    changes.append(f"Current listings sample: {current_jobs[:300]}")
            else:
                changes.append(f"First jobs snapshot. Sample: {current_jobs[:300]}")

            save_snapshot("jobs_snapshots", comp_name, jobs_raw=current_jobs)

            if changes:
                all_signals.append({
                    "competitor": comp_name,
                    "source": "jobs",
                    "changes": changes
                })

        except Exception as e:
            print(f"Error scraping jobs for {comp_name}: {e}")

    return all_signals