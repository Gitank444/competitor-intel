from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

COMPETITORS = [
    {
        "name": "Woebot",
        "github_org":None,
        "docs_url": "https://woebothealth.com",
        "blog_rss": None,
        "jobs_url": "https://woebothealth.com/careers/",
    },
    {
        "name": "Wysa",
        "github_org": None,
        "docs_url": "https://www.wysa.com",
        "blog_rss": None,
        "jobs_url": "https://www.wysa.com/careers",
    },
]