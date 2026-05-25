import requests
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

API_KEY = "4c1500aa70234c43bfe8562620948dc0"

url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

response = requests.get(url)

data = response.json()

articles = data["articles"]

analyzer = SentimentIntensityAnalyzer()

final_data = []

for article in articles:

    author = article.get("author")
    description = article.get("description")
    published_date = article.get("publishedAt")

    if description:

        score = analyzer.polarity_scores(description)

        sentiment_score = score["compound"]

        news = {
            "author": author,
            "published_date": published_date,
            "description": description,
            "sentiment_score": sentiment_score
        }

        final_data.append(news)

print(json.dumps(final_data, indent=4))

with open("news.json", "w") as f:
    json.dump(final_data, f, indent=4)

print("Filtered news data stored")