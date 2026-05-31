from firecrawl import FirecrawlApp
from config import FIRECRAWL_API_KEY, COMPETITORS
from storage.db import get_last_snapshot, save_snapshot
import difflib

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def collect_docs_signals():
    all_signals = []

    for competitor in COMPETITORS:
        comp_name = competitor.get("name")
        docs_url = competitor.get("docs_url")

        if not docs_url:
            continue

        print(f"Collecting docs for {comp_name}...")

        try:
            result = app.scrape_url(docs_url, formats=["markdown"])
            current_content = result.markdown or ""
            print(f"{comp_name} docs length: {len(current_content)}")
            
            last = get_last_snapshot("docs_snapshots", comp_name)
            changes = []

            if last:
                diff = list(difflib.unified_diff(
                    last[3].splitlines(),
                    current_content.splitlines(),
                    lineterm=""
                ))
                if diff:
                    added = [l for l in diff if l.startswith("+") and not l.startswith("+++")]
                    removed = [l for l in diff if l.startswith("-") and not l.startswith("---")]
                    changes.append(f"{len(added)} lines added, {len(removed)} lines removed")
                    if added:
                        changes.append("Sample new content: " + " | ".join(added[:3]))
                # else:
                #     changes.append(f"No changes but snapshot exists. Sample: {current_content[:300]}")
            else:
                # changes.append(f"First docs snapshot. Sample: {current_content[:300]}")
                changes.append(f"First snapshot for docs. Sample: ({len(current_content)} chars) ")
                
                if current_content:
                    "Sample content: " + current_content[:300].replace("\n", " ")

            save_snapshot("docs_snapshots", comp_name, url=docs_url, content=current_content)

            if changes:
                all_signals.append({
                    "competitor": comp_name,
                    "source": "docs",
                    "changes": changes
                })

        except Exception as e:
            print(f"Error scraping docs for {comp_name}: {e}")

    return all_signals