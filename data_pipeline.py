import requests
import mysql.connector
from datetime import datetime, timedelta
import os
from dateutil import parser
import html
import re
API_KEY = "b11e8c0730aa42768214c10680800841"  # Replace with your actual API key



def clean(text):
    if not text:
        return ""
    text = html.unescape(text)  # Decode HTML entities
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'{.*?}', '', text)  # Remove JS artifacts
    return text.strip()


def fetch_and_store_news():
    # Get today's date
    from_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    url = f"https://newsapi.org/v2/everything?q=India+AND+AI&from={from_date}&sortBy=publishedAt&apiKey={API_KEY}"



    resp = requests.get(url)
    print("Status Code:", resp.status_code)
    print("Response:", resp.text)
    data = resp.json()
    articles = data.get("articles", [])

    # MySQL connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Change if needed
        password="root",  # Change if needed
        database="rag_db"
    )
    cursor = conn.cursor()

    for article in articles:
        title = clean(article.get("title", ""))
        content = clean(article.get("content", ""))
        published_at_raw = article.get("publishedAt", from_date)
        try:
            published_at = parser.parse(published_at_raw).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            published_at = from_date + " 00:00:00"

        try:
            cursor.execute(
                "INSERT INTO news (title, content, published_at) VALUES (%s, %s, %s)",
                (title, content, published_at)
            )
        except Exception as e:
            print("Error inserting:", e)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(articles)} articles.")

if __name__ == "__main__":
    fetch_and_store_news()
