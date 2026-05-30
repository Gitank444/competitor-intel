from storage.db import init_db
from collectors.github_collector import collect_github_signals
from collectors.docs_collector import collect_docs_signals
from collectors.jobs_collector import collect_jobs_signals
from analyzer.summarizer import summarize_signals
from delivery.slack_notifier import send_to_slack

def run_pipeline():
    print("Initializing database...")
    init_db()

    print("Collecting signals...")
    github_signals = collect_github_signals()
    docs_signals = collect_docs_signals()
    jobs_signals = collect_jobs_signals()

    all_signals = github_signals + docs_signals + jobs_signals
    print(f"Total signals collected: {len(all_signals)}")

    print("Analyzing signals...")
    summary = summarize_signals(all_signals)

    print("Delivering digest...")
    send_to_slack(summary)

    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()