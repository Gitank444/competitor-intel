import anthropic
from config import ANTHROPIC_API_KEY
import json

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def summarize_signals(all_signals):
    if not all_signals:
        return "No changes detected this week across all competitors."

    signals_text = json.dumps(all_signals, indent=2)

    prompt = f"""You are a competitive intelligence analyst for a startup.

Below are raw signals collected this week from competitor monitoring across GitHub, documentation, and job postings.

Your job:
1. For each competitor, summarize what changed
2. Identify what they are likely building based on these signals
3. Flag anything urgent the product or engineering team should know
4. Keep the entire summary under 400 words
5. Be direct and specific, no fluff

Raw signals:
{signals_text}

Output format:
COMPETITOR NAME
- What changed: ...
- What they're likely building: ...
- Urgency flag (if any): ...

---
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text