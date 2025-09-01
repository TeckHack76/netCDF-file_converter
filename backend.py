import pandas as pd
import sqlite3

# Load processed CSV
df = pd.read_csv("processed.csv")

# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect("argo.db")

# Save dataframe into DB
df.to_sql("measurements", conn, if_exists="replace", index=False)

conn.close()
print("✅ Data saved to argo.db")