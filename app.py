import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Polygon.io API Key (Replace with your own)
API_KEY = "tktev3i3JKQrLqNPTdxf14r_MX_wpcr0"

# Function to fetch financials from Polygon API
def get_fundamentals(ticker, limit=10):
    url = f"https://api.polygon.io/vX/reference/financials?ticker={ticker}&limit={limit}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error("Error fetching data. Check API key or ticker.")
        return []

# Streamlit UI
st.set_page_config(page_title="Fundamental Analysis Dashboard", layout="wide")

st.title("📊 Fundamental Analysis Dashboard")
st.sidebar.header("Enter Stock Ticker")

# User input
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL)", "AAPL").upper()

# Fetch data
data = get_fundamentals(ticker)

if data:
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Show raw financials
    st.subheader(f"Financial Data for {ticker}")
    st.dataframe(df)

    # Select key financial metrics
    key_metrics = ["calendarDate", "revenue", "netIncome", "eps", "operatingExpenses", "grossProfit"]

    if not df.empty and all(col in df.columns for col in key_metrics):
        df_filtered = df[key_metrics].dropna()

        # Plot revenue trend
        fig = px.line(df_filtered, x="calendarDate", y="revenue", title="Revenue Trend", markers=True)
        st.plotly_chart(fig)

        # Plot net income trend
        fig = px.line(df_filtered, x="calendarDate", y="netIncome", title="Net Income Trend", markers=True)
        st.plotly_chart(fig)

        # Plot EPS trend
        fig = px.line(df_filtered, x="calendarDate", y="eps", title="EPS Trend", markers=True)
        st.plotly_chart(fig)
else:
    st.warning("No financial data available for this ticker.")
