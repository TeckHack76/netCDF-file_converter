import sqlite3
import pandas as pd


def query_to_sql(user_query: str):
    q = user_query.lower()

    if "band1" in q or "temperature" in q:
        return "SELECT lat, lon, band1 FROM measurements LIMIT 2000;"
    elif "band2" in q or "salinity" in q:
        return "SELECT lat, lon, band2 FROM measurements LIMIT 2000;"
    elif "band3" in q:
        return "SELECT lat, lon, band3 FROM measurements LIMIT 2000;"
    elif "band4" in q:
        return "SELECT lat, lon, band4 FROM measurements LIMIT 2000;"
    elif "band5" in q:
        return "SELECT lat, lon, band5 FROM measurements LIMIT 2000;"
    else:
        return None


def run_query(sql):
    conn = sqlite3.connect("argo.db")
    df = pd.read_sql(sql, conn)
    conn.close()
    return df
