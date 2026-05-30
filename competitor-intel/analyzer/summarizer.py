from groq import Groq
from config import GROQ_API_KEY
import json

client = Groq(api_key=GROQ_API_KEY)

def summarize_signals(current_signals, historical_signals=None):
    if not current_signals:
        return "No changes detected this week across all competitors."

    current_signals_text = json.dumps(current_signals, indent=2)

    prompt = f"""You are a senior competitive intelligence analyst for a mental health startup.

You have signals collected this week from competitor monitoring across docs and job postings.

Rules:
- Never report a single signal in isolation
- Correlate across sources before making a claim
- If only one signal exists, say "insufficient signal, monitoring"
- Assign a probability: High / Medium / Low that a specific product move is happening
- Be specific about WHAT they are likely building
- Flag urgency only if it directly threatens your product or opens an opportunity

Current week signals:
{current_signals_text}

Output format per competitor:

COMPETITOR NAME
Signal summary: [what changed across all sources this week]
Hypothesis: [what they are likely building and why]
Probability: [High / Medium / Low] — [one line reasoning]
Action recommended: [what your product team should do, or "monitor"]
"""

    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.choices[0].message.content