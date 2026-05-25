import streamlit as st
import pandas as pd
import pg8000

st.set_page_config(layout="wide")

st.title("News Analytics Sentiment Score Dashboard")

# database connection
conn = pg8000.connect(
    host="host",
    database="postgres",
    user="postgres",
    password="password",
    port="5432",
    # sslmode="require"
)

query = "SELECT * FROM news_data"

df = pd.read_sql(query, conn)

conn.close()

# color sentiment score
def color_score(val):

    if val > 0:
        return "background-color: green; color: white"

    elif val < 0:
        return "background-color: red; color: white"

    else:
        return "background-color: gray; color: white"

styled_df = df.style.map(color_score, subset=["sentiment_score"])

# show table
st.dataframe(styled_df, use_container_width=True)
