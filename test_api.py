import requests
import json

API_KEY = "api_key"

url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

response = requests.get(url)

data = response.json()

# full response print
print(json.dumps(data, indent=4))

# articles only
articles = data["articles"]

print("\nTotal Articles:", len(articles))

for article in articles:
    print("\n-------------------")
    print("Title:", article.get("title"))
    print("Author:", article.get("author"))
    print("Description:", article.get("description"))
    print("Published At:", article.get("publishedAt"))