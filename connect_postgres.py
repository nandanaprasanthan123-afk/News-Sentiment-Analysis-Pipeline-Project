import json
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="newsdb",
    user="postgres",
    password="root"
)

cur = conn.cursor()

with open("news.json", "r") as f:
    data = json.load(f)

for article in data:

    author = article["author"]
    published_date = article["published_date"]
    description = article["description"]
    sentiment_score = article["sentiment_score"]

    query = """
    INSERT INTO news_dataa
    (author, published_date, description, sentiment_score)
    VALUES (%s, %s, %s, %s)
    """

    values = (author, published_date, description, sentiment_score)

    cur.execute(query, values)

conn.commit()

print("Data inserted successfully")

cur.close()
conn.close()