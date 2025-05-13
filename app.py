from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import ollama
import json

app = FastAPI()

# CORS for local HTML frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    user_input: str

def query_news(keywords: str):
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="rag_db"
    )
    cursor = conn.cursor()
    sql = (
        "SELECT title, content FROM news "
        "WHERE MATCH(title, content) AGAINST (%s IN NATURAL LANGUAGE MODE) "
        "ORDER BY published_at DESC LIMIT 3"
    )
    cursor.execute(sql, (keywords,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


@app.post("/chat")
async def chat(q: Query):
    # SYSTEM PROMPT: Tell LLM to use tool if needed
    system = (
    "You are a helpful assistant with access to a tool called: "
    "query_news(keywords: str) -> list of news articles. "
    "When the user asks about any current event, public figure, news topic, date, country, or article, "
    "you MUST call this function using keywords from the question like this: "
    '{"function": "query_news", "args": {"keywords": "relevant keywords here"}}. '
    "Do not guess the answer — always use the function if the user asks about the news." 
    )

    # Call Ollama LLM 
    response = ollama.chat(
        model="qwen:0.5b", 
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": q.user_input}
        ],
        options={"tools": [
            {
                "name": "query_news",
                "description": "Searches news articles",
                "parameters": {
                    "keywords": {"type": "string", "description": "keywords to search"}
                }
            }
        ]}
    )

    # Parse LLM tool call if exists
    try:
        tool_call = json.loads(response["message"]["content"])
        print("Tool call received:", tool_call)

        if tool_call.get("function") == "query_news":
            keywords = tool_call["args"]["keywords"]
            results = query_news(keywords)
            if not results:
                return {"response": "No news found for your query."}
            # Summarize for user
            summary = "\n\n".join([f"Title: {r[0]}\nContent: {r[1]}" for r in results])
            return {"response": summary}
    except Exception:
        pass

    # If no tool call, return LLM's own answer
    return {"response": response["message"]["content"]}
