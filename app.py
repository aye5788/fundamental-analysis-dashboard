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

# Extract key financial metrics
def extract_metrics(data):
    records = []
    for item in data:
        financials = item.get("financials", {})
        balance_sheet = financials.get("balance_sheet", {})
        income_statement = financials.get("income_statement", {})
        cash_flow = financials.get("cash_flow_statement", {})
        
        records.append({
            "date": item.get("start_date", ""),
            "fiscal_period": item.get("fiscal_period", ""),
            "revenue": income_statement.get("revenue", {}).get("value"),
            "net_income": income_statement.get("net_income", {}).get("value"),
            "eps": income_statement.get("eps", {}).get("value"),
            "total_assets": balance_sheet.get("total_assets", {}).get("value"),
            "total_liabilities": balance_sheet.get("total_liabilities", {}).get("value"),
            "cash_from_operations": cash_flow.get("net_cash_flow_from_operations", {}).get("value"),
        })
    return pd.DataFrame(records)

# Streamlit UI
st.set_page_config(page_title="Fundamental Analysis Dashboard", layout="wide")
st.title("📊 Fundamental Analysis Dashboard")
st.sidebar.header("Enter Stock Ticker")

# User input
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL)", "AAPL").upper()

# Fetch and process data
data = get_fundamentals(ticker)
df = extract_metrics(data)

if not df.empty:
    st.subheader(f"Key Financials for {ticker}")
    st.dataframe(df)

    # Plot Revenue Trend
    fig = px.line(df, x="date", y="revenue", title=f"📈 {ticker} Revenue Trend", markers=True)
    st.plotly_chart(fig)

    # Plot Net Income Trend
    fig = px.line(df, x="date", y="net_income", title=f"💰 {ticker} Net Income Trend", markers=True)
    st.plotly_chart(fig)

    # Plot EPS Trend
    fig = px.line(df, x="date", y="eps", title=f"📊 {ticker} Earnings Per Share (EPS)", markers=True)
    st.plotly_chart(fig)
    
else:
    st.warning("No useful financial data available for this ticker.")

