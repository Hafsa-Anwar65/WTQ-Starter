"""Keep every prompt here so you can tweak quickly during the event."""

SYSTEM = (
    "You are an expert assistant embedded in a product. "
    "Be accurate, concise, and base answers only on the data provided. "
    "If the data does not contain the answer, say so instead of guessing."
)

# Example structured-output prompt; adapt to the challenge on the day.
ANALYZE_TEMPLATE = """Analyze the following input and respond as JSON with this schema:
{{
  "summary": "one or two sentences",
  "key_points": ["..."],
  "risk_or_score": 0-100,
  "recommended_action": "..."
}}

INPUT:
{user_input}

CONTEXT FROM DATASET:
{context}
"""
