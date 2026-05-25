def lambda_handler(event, context):

    import urllib.request
    import json
    import pg8000
    import boto3
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    from datetime import datetime

    # ---------------- NEWS API ----------------
    API_KEY = "4c1500aa70234c43bfe8562620948dc0"
    
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    if data.get("status") != "ok":
        print("API ERROR:", data)

        return {
            "statusCode": 500,
            "body": json.dumps(data)
        }

    articles = data.get("articles", [])
    print("Articles fetched:", len(articles))

    # ---------------- SENTIMENT ----------------
    analyzer = SentimentIntensityAnalyzer()
    final_data = []

    # ---------------- RDS CONNECTION ----------------
    conn = pg8000.connect(
        host="newsdb.cvuk0ousc90q.ap-south-1.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="nandanakk",
        port="5432"
    )

    cur = conn.cursor()

    # ---------------- CREATE TABLE ----------------
    create_table_query = """
    CREATE TABLE IF NOT EXISTS news_data (
        id SERIAL PRIMARY KEY,
        author TEXT,
        published_date TIMESTAMP,
        description TEXT,
        sentiment_score FLOAT
    )
    """

    cur.execute(create_table_query)
    conn.commit()

    # ---------------- PROCESS ARTICLES ----------------
    for article in articles:

        try:
            author = article.get("author")
            description = article.get("description")
            published_date = article.get("publishedAt")

            if not description:
                continue

            if published_date:
                published_date = datetime.strptime(
                    published_date,
                    "%Y-%m-%dT%H:%M:%SZ"
                )

            sentiment_score = analyzer.polarity_scores(description)["compound"]

            news = {
                "author": author,
                "published_date": str(published_date),
                "description": description,
                "sentiment_score": sentiment_score
            }

            final_data.append(news)

            query = """
            INSERT INTO news_data
            (author, published_date, description, sentiment_score)
            VALUES (%s, %s, %s, %s)
            """

            cur.execute(query, (
                author,
                published_date,
                description,
                sentiment_score
            ))

            conn.commit()

            cur.execute("SELECT COUNT(*) FROM public.news_data")
            count = cur.fetchone()[0]

            print("CURRENT ROW COUNT:", count)

        except Exception as e:
            print("INSERT ERROR:", e)
            conn.rollback()

    # ---------------- S3 SETUP ----------------
    s3 = boto3.client("s3", region_name="ap-south-1")

    bucket_name = "newsapi-bucket-11"

    # ---------------- UPLOAD TO S3 ----------------
    try:

        file_name = f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(final_data)
        )

        print(f"Uploaded to S3: {file_name}")

    except Exception as e:
        print("S3 ERROR:", e)

    # ---------------- CLOSE CONNECTION ----------------
    cur.close()
    conn.close()

    print("DONE: News stored in RDS + S3")

    return {
        "statusCode": 200,
        "body": json.dumps("Success")
    }