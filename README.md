# Ai Support Assistant (LangChain + Gemini API + Flask)

A web-based AI customer support assistant that answers FAQs using LangChain and Google's Gemini API. Built with Flask for the backend and vanilla HTML/CSS/JS for the frontend. Gemini's free tier requires no credit card, so this runs at zero cost.

## Features

- Web chat interface (type a message, get a response)
- Maintains conversation context during a session
- "Reset" button to clear the conversation
- Responses grounded in a company FAQ/policy block passed to the model
- Errors (missing key, API failures) shown clearly in the UI

## Tech Stack

- Python 3.9+
- Flask
- LangChain (`langchain`, `langchain-google-genai`, `langchain-core`)
- python-dotenv for environment variables

## Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-url>
cd AI-Customer-Support-Assistant
```

### 2. Create and activate a virtual environment

```
python3 -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure your API key

1. Get a free Gemini API key (no credit card required) at https://aistudio.google.com/apikey
2. Create a `.env` file in the project root:

```
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxx
```

### 5. Run the app

```
python app.py
```

Open your browser at http://127.0.0.1:5000

## Project Structure

```
AI-Customer-Support-Assistant/
├── app.py                  # Flask backend, LangChain + Gemini chat chain
├── templates/
│   └── index.html          # Chat UI markup, styling, and frontend JS
├── requirements.txt        # Python dependencies
├── .env                    # Your Gemini API key (not committed)
├── .gitignore
└── README.md
```

## How It Works

1. The user types a message in the browser and hits Send.
2. The frontend (inline JS in `index.html`) sends a POST request to `/api/chat`.
3. Flask (`app.py`) builds a LangChain prompt (system instructions + company FAQ context + conversation history) and invokes it against `gemini-2.5-flash` via `ChatGoogleGenerativeAI`.
4. The reply is appended to an in-memory conversation history and returned as JSON, then rendered in the chat window.

## Usage Guide

1. Make sure the app is running (see Setup Instructions above) and http://127.0.0.1:5000 is open in your browser.
2. Type a message in the input box at the bottom and press Send.
3. The assistant's response will appear in the chat window above.
4. Continue the conversation — the assistant remembers earlier messages in the same session.
5. Click **Reset** at the top to clear the conversation and start fresh.

## Notes

- Company info/policies live in the `FAQ_CONTEXT` string in `app.py` — edit it to match real policies.
- Chat history is kept in-memory per server process (single-session demo, not multi-user safe).
- Gemini's free tier has per-minute and per-day request limits. If you see a `429 RESOURCE_EXHAUSTED` error, wait a bit before sending another message, or check current usage at https://ai.dev/rate-limit.
