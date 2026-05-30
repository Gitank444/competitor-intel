from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

COMPETITORS = [
    {
        "name": "CompetitorOne",
        "github_org": "competitor-one-org",
        "docs_url": "https://docs.competitorone.com",
        "blog_rss": "https://competitorone.com/blog/rss.xml",
        "jobs_url": "https://competitorone.com/careers",
    },
]