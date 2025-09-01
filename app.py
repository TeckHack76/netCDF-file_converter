import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ------------------------------
# Database helper functions
# ------------------------------

def query_to_sql(user_query: str):
    """Convert simple English queries into SQL queries"""
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
    """Run SQL query on SQLite database and return DataFrame"""
    conn = sqlite3.connect("argo.db")
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


# ------------------------------
# Streamlit App
# ------------------------------

st.set_page_config(page_title="FloatChat – Ocean Data Explorer", layout="wide")
st.title("🌊 FloatChat – Ocean Data Explorer")

st.write("Ask questions about ARGO ocean data and see visualizations instantly!")

# Textbox for user query
query = st.text_input("💬 Type your query (try 'show band1' or 'show salinity'):")

if query:
    sql = query_to_sql(query)  # English → SQL
    if sql:
        st.write("🔎 SQL Generated:", sql)

        with st.spinner("Fetching data..."):
            df_result = run_query(sql)

        # Show table preview
        st.subheader("📋 Data Preview")
        st.write(df_result.head())

        # Identify which band column is present
        band_col = [c for c in df_result.columns if "band" in c][0]

        # Plot scatter chart
        st.subheader(f"📊 Scatter Visualization for {band_col}")
        fig = px.scatter(df_result, x="lon", y="lat", color=band_col,
                         title=f"{band_col} Visualization")
        st.plotly_chart(fig, use_container_width=True)

        # 🌍 World Map
        st.subheader(f"🌍 Global Map for {band_col}")
        fig_geo = px.scatter_geo(df_result, lat="lat", lon="lon", color=band_col,
                                 projection="natural earth",
                                 title=f"{band_col} Global Distribution")
        st.plotly_chart(fig_geo, use_container_width=True)

        # 📊 Summary Stats
        st.subheader("📈 Summary Statistics")
        st.write({
            "min": float(df_result[band_col].min()),
            "max": float(df_result[band_col].max()),
            "mean": float(df_result[band_col].mean())
        })

    else:
        st.warning("❌ Sorry, I don’t understand that query yet. Try 'show band1' or 'show band2'.")

# ------------------------------
# Extra Features (Quick Wins)
# ------------------------------

st.markdown("---")
st.subheader("✨ Quick Demo Buttons")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Show Band1"):
        df = run_query("SELECT lat, lon, band1 FROM measurements LIMIT 2000;")
        fig = px.scatter(df, x="lon", y="lat", color="band1", title="Band1 Visualization")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if st.button("Show Band2"):
        df = run_query("SELECT lat, lon, band2 FROM measurements LIMIT 2000;")
        fig = px.scatter(df, x="lon", y="lat", color="band2", title="Band2 Visualization")
        st.plotly_chart(fig, use_container_width=True)

with col3:
    if st.button("Show Band3"):
        df = run_query("SELECT lat, lon, band3 FROM measurements LIMIT 2000;")
        fig = px.scatter(df, x="lon", y="lat", color="band3", title="Band3 Visualization")
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Dropdown for easy switching
# ------------------------------
st.markdown("---")
st.subheader("📌 Select Band from Dropdown")

option = st.selectbox("Choose a variable to visualize:", ["band1", "band2", "band3", "band4", "band5"])
df = run_query(f"SELECT lat, lon, {option} FROM measurements LIMIT 2000;")

fig = px.scatter(df, x="lon", y="lat", color=option, title=f"{option} Scatter Plot")
st.plotly_chart(fig, use_container_width=True)

fig_geo = px.scatter_geo(df, lat="lat", lon="lon", color=option,
                         projection="natural earth",
                         title=f"{option} Global Map")
st.plotly_chart(fig_geo, use_container_width=True)

st.write("📈 Stats:", {
    "min": float(df[option].min()),
    "max": float(df[option].max()),
    "mean": float(df[option].mean())
})
