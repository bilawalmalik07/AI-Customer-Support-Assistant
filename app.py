import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

FAQ_CONTEXT = """
Company: BrightGear Electronics
Support policies:
- Returns accepted within 30 days of purchase with receipt.
- Standard shipping takes 5-7 business days; express takes 1-2 business days.
- Warranty: 1 year manufacturer warranty on all products.
- Refunds are processed within 5-10 business days after the returned item is received.
- Customers can track orders using the order ID on the "Track Order" page.
- Support hours: Mon-Fri, 9am-6pm EST. Email: support@brightgear.example
- Damaged/defective items can be exchanged free of charge within 30 days.
- Cancellations are allowed only if the order has not yet shipped.
"""

SYSTEM_PROMPT = f"""You are a professional, friendly customer support assistant for BrightGear Electronics.
Answer customer questions accurately using the company info below. If something isn't covered by
the info, say you don't have that information and suggest contacting support@brightgear.example.
Keep answers concise and professional.

Company info:
{FAQ_CONTEXT}
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm

app = Flask(__name__)

# in-memory session history (single session, simple demo)
chat_history = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not set on server"}), 500

    response = chain.invoke({"input": user_message, "history": chat_history})
    reply = response.content

    chat_history.append(HumanMessage(content=user_message))
    chat_history.append(AIMessage(content=reply))
    # keep history bounded
    if len(chat_history) > 20:
        del chat_history[:2]

    return jsonify({"reply": reply})


@app.route("/api/reset", methods=["POST"])
def reset():
    chat_history.clear()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
