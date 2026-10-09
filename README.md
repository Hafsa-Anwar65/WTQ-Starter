# WTQ 2026 – Project Title

**Problem:** (who is affected, what hurts)
**Solution:** (what the app does, in one sentence)
**Impact:** (time/money saved, who benefits)

## Model used
`<model-id>` via `<provider>` (allowed WTQ 2026 model)

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # then add your API key
python test_llm.py            # verify key works
streamlit run app.py
```

## How it works
1. User provides input (and/or dataset)
2. App builds a grounded prompt from the data
3. LLM returns structured JSON
4. UI renders summary, key points, score and recommended action

## Reliability
- Input validation, retries with backoff, graceful error messages
- Structured JSON output parsing with fallback

## Demo
(link to screen recording)
