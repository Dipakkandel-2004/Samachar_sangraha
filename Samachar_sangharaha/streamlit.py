import streamlit as st
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="samachar_sangraha",
    user="postgres",
    password="admin",
    port=5432,
)
query = "SELECT * From news ORDER BY published_date DESC"
unique_source = "SELECT distinct source_name from news"
unique_source_df = pd.read_sql(unique_source, conn)
df = pd.read_sql(query, conn)
print(unique_source_df)
for index, row in df.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {row['title']}")
        st.write(row["description"])
        st.write(row["source_link"])
    with col2:
        st.caption(f"Published: {row['published_date']}")
        st.caption(f"Source: {row['source_name']}")
    st.markdown("---")
