import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

# Function to fetch NIFTY50 stock symbols
def get_nifty50_symbols():
    return [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "ADANIENT.NS", "HDFC.NS",
        "KOTAKBANK.NS", "ITC.NS", "LT.NS", "WIPRO.NS", "TITAN.NS",
        "ASIANPAINT.NS", "ULTRACEMCO.NS", "AXISBANK.NS", "DMART.NS", "MARUTI.NS",
        "SUNPHARMA.NS", "TECHM.NS", "HCLTECH.NS", "NTPC.NS", "POWERGRID.NS",
        "JSWSTEEL.NS", "TATAMOTORS.NS", "ONGC.NS", "COALINDIA.NS", "ADANIPORTS.NS",
        "GRASIM.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "M&M.NS", "EICHERMOT.NS",
        "BPCL.NS", "DIVISLAB.NS", "SHREECEM.NS", "NESTLEIND.NS", "CIPLA.NS",
        "SBILIFE.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "BRITANNIA.NS", "TATASTEEL.NS",
        "UPL.NS", "INDUSINDBK.NS", "DRREDDY.NS", "APOLLOHOSP.NS", "BAJAJ-AUTO.NS"
    ]

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate MACD
def calculate_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# Function to analyze a stock
def analyze_stock(ticker):
    data = yf.download(ticker, period="1mo", interval="15m")
    data['RSI'] = calculate_rsi(data)
    data['MACD'], data['Signal'] = calculate_macd(data)
    
    # Trading suggestion logic
    last_rsi = data['RSI'].iloc[-1]
    last_macd = data['MACD'].iloc[-1]
    last_signal = data['Signal'].iloc[-1]
    
    if last_rsi < 30 and last_macd > last_signal:
        suggestion = "Buy"
    elif last_rsi > 70 and last_macd < last_signal:
        suggestion = "Sell"
    else:
        suggestion = "Hold"
    
    return {
        "RSI": last_rsi,
        "MACD": last_macd,
        "Signal": last_signal,
        "Suggestion": suggestion
    }

# Streamlit App
st.title("NIFTY50 Intraday Trading Analyzer")

nifty50_symbols = get_nifty50_symbols()
selected_ticker = st.selectbox("Select a stock from NIFTY50:", nifty50_symbols)

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing data..."):
        analysis = analyze_stock(selected_ticker)
    
    st.write(f"### Analysis for {selected_ticker}")
    st.write(f"**RSI:** {analysis['RSI']:.2f}")
    st.write(f"**MACD:** {analysis['MACD']:.2f}")
    st.write(f"**Signal:** {analysis['Signal']:.2f}")
    st.write(f"**Trading Suggestion:** {analysis['Suggestion']}")
    
    # Fetch and display candlestick chart
    data = yf.download(selected_ticker, period="1mo", interval="15m")
    st.line_chart(data[['Close']])

st.write("Note: This is a tool for educational purposes only. Trade responsibly!")
