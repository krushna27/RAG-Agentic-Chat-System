# RAG Agentic Chat System – NewsAPI Edition

This project is a Retrieval-Augmented Generation (RAG) chat application that uses a local LLM (Ollama) and NewsAPI data to answer user queries based on the most recent news articles. It combines a data ingestion pipeline, a MySQL database, FastAPI backend, and a basic HTML chat frontend to simulate an intelligent agent capable of retrieving and summarizing data.


✔️ Daily Updating Data Pipeline
News data is pulled daily using NewsAPI and stored in MySQL.
The data_pipeline.py script fetches articles with keyword "AI" and persists them locally.

✔️ Agentic LLM with Tool Calls
The LLM is guided via a system prompt to call a function query_news(keywords: str) to retrieve relevant news.
Tool schema is defined and returned tool calls are parsed and executed.

✔️ MySQL Integration (Raw Queries)
All queries to the database use raw SQL — no ORMs are used.
MySQL stores article title, content, and publish timestamp.

✔️ FastAPI Backend
Handles POST requests to /chat endpoint.
Accepts user queries and returns either an LLM response or a function-derived answer.

✔️ HTML Chat UI
Minimal HTML page with a query input box and a scrollable history pane.
Allows users to chat with the RAG agent via a clean interface.



 # Getting Started
# 1.  Clone the Repository

# 2.  Set up MySQL Database
Create a MySQL database and table:

CREATE DATABASE rag_db;
USE rag_db;

CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    content TEXT,
    published_at DATETIME
);

# 3. Install Requirements
pip install fastapi mysql-connector-python requests pydantic uvicorn

# 4. Pull Ollama Model
Make sure you have Ollama installed, then:
ollama pull qwen2:0.5b

# 5. Run Data Pipeline
python data_pipeline.py

# 6. Start FastAPI Server
uvicorn app:app --reload

# 7. Open index.html
Open the HTML file in a browser. You can now chat with the LLM-powered agent.



# Option: LM Studio
Download LM Studio
Download a chat model (e.g., Mistral, Llama, Gemma, etc.)
Enable the OpenAI-compatible API server 

# Option:GPT4All
Download GPT4All
Download a model and start the local server.



LM Studio/GPT4All:

In app.py, replace the Ollama call with:

import openai

openai.api_base = "http://localhost:1234/v1"  # LM Studio default
openai.api_key = "not-needed"

response = openai.ChatCompletion.create(
    model="your-model-name",
    messages=[{"role": "user", "content": "Your prompt here"}]
)

# Usage
- Type a question in the chat box (e.g., "What are the latest AI news?").

- The agent will decide whether to search the database or answer directly.

- Tool calls (database queries) are hidden from the user.
