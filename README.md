# BrightGear Support Assistant

LangChain + Gemini customer support chatbot with a Flask web UI.

## Setup

```
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
python app.py
```

Open http://localhost:5000

## Notes
- FAQ/company info is in the `FAQ_CONTEXT` string in `app.py` — edit it to match your real policies.
- Chat history is kept in-memory per server process (single session demo, not multi-user safe).
- Swap `model="gemini-2.0-flash"` in `app.py` for another Gemini model if needed.
