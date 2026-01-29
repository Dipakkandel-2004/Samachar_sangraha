import psycopg2
import csv
import os
from pathlib import Path

folder = "c:/Users/kande/Desktop/Samachar_sangharaha"
conn = psycopg2.connect(
    host="localhost",
    database="samachar_sangraha",
    user="postgres",
    password="admin",
    port="5432",
)

csv_files = [f for f in os.listdir(folder) if f.endswith(".csv")]

cursor = conn.cursor()
print("Connected successfully")
for file in csv_files:
    with open(file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if not row:
                continue
            cursor.execute(
                """

                INSERT INTO news (title,published_date,description,source_name,source_link)
                VALUES (%s, %s, %s, %s,%s)
                """,
                row,
            )

conn.commit()
cursor.close()
conn.close()
for file in csv_files:
    file_path = Path(file)
    if file_path.exists():
        file_path.unlink()
