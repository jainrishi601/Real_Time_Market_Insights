import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import time
import talib

# Function to fetch candlestick data
def fetch_candlestick_data(ticker, period, interval):
    data = yf.download(tickers=ticker, period=period, interval=interval)
    return data

# Function to plot line chart
def plot_line_chart(data, fig):
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Closing Price'))

# Function to plot candlestick chart
def plot_candlestick(data, fig, patterns):
    fig.add_trace(go.Candlestick(x=data.index,
                                  open=data.iloc[:, 0],
                                  high=data.iloc[:, 1],
                                  low=data.iloc[:, 2],
                                  close=data.iloc[:, 3], name='Candlestick'))

    for pattern_name, pattern_info in patterns.items():
        for index in pattern_info["Indices"]:
            fig.add_annotation(
                x=data.index[index],
                y=data.iloc[:, 1][index],
                xref="x",
                yref="y",
                text=f"{index}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )


# Function to detect candlestick patterns and predict market movement
def detect_candlestick_patterns(data):
    patterns = {}
    candlestick_functions = [func for func in dir(talib) if func.startswith('CDL')]
    
    for func_name in candlestick_functions:
        func = getattr(talib, func_name)
        pattern = func(data['Open'], data['High'], data['Low'], data['Close'])
        new_indices = np.where(pattern != 0)[0]
        if any(new_indices):
            patterns[func_name[3:]] = new_indices
    
    bullish_patterns = [
    "CDL3LINESTRIKE", "CDLINVERTEDHAMMER", "CDL3WHITESOLDIERS", "CDLHOMINGPIGEON",
    "CDL3INSIDE", "CDLIDENTICAL3CROWS", "CDLINNECK", "CDLHARAMI",
    "CDLHARAMICROSS", "CDLRISEFALL3METHODS", "CDLKICKING", "CDLKICKINGBYLENGTH",
    "CDLUNIQUE3RIVER", "CDL3STARSINSOUTH", "CDLMORNINGDOJISTAR", "CDLMORNINGSTAR",
    "CDLPIERCING", "CDLABANDONEDBABY", "CDLADVANCEBLOCK", "CDLBELTHOLD", "CDLBREAKAWAY",
    "CDLCLOSINGMARUBOZU", "CDLCONCEALBABYSWALL", "CDLCOUNTERATTACK", "CDLDARKCLOUDCOVER",
    "CDLENGULFING", "CDLGAPSIDESIDEWHITE", "CDLHAMMER", "CDLHANGINGMAN", "CDLHARAMI",
    "CDLHIGHWAVE", "CDLHIKKAKE", "CDLHIKKAKEMOD", "CDLLADDERBOTTOM", "CDLMATCHINGLOW",
    "CDLMATHOLD", "CDLONNECK", "CDLTHRUSTING", "CDLTRISTAR", "CDLUPSIDEGAP2CROWS"
]

    bearish_patterns = [
    "CDL3BLACKCROWS", "CDL3LINESTRIKE", "CDL3OUTSIDE",
    "CDL3STARSINSOUTH", "CDLABANDONEDBABY", "CDLADVANCEBLOCK", "CDLBELTHOLD",
    "CDLBREAKAWAY", "CDLCLOSINGMARUBOZU", "CDLCONCEALBABYSWALL", "CDLCOUNTERATTACK",
    "CDLDARKCLOUDCOVER", "CDLENGULFING", "CDLGAPSIDESIDEWHITE", "CDLGRAVESTONEDOJI",
    "CDLHAMMER", "CDLHANGINGMAN", "CDLHARAMI", "CDLHARAMICROSS", "CDLHIGHWAVE",
    "CDLHIKKAKE", "CDLHIKKAKEMOD", "CDLHOMINGPIGEON", "CDLIDENTICAL3CROWS", "CDLINNECK",
    "CDLKICKING", "CDLKICKINGBYLENGTH", "CDLLADDERBOTTOM", "CDLLONGLEGGEDDOJI", "CDLLONGLINE",
    "CDLMARUBOZU", "CDLMATCHINGLOW", "CDLMATHOLD", "CDLMORNINGDOJISTAR", "CDLMORNINGSTAR",
    "CDLONNECK", "CDLPIERCING", "CDLRICKSHAWMAN", "CDLRISEFALL3METHODS", "CDLSEPARATINGLINES",
    "CDLSHOOTINGSTAR", "CDLSHORTLINE", "CDLSTALLEDPATTERN", "CDLSTICKSANDWICH", "CDLTAKURI",
    "CDLTASUKIGAP", "CDLTHRUSTING", "CDLTRISTAR", "CDLUPSIDEGAP2CROWS"
]
    neutral_patterns = [
    "CDLDOJI", "CDLDOJISTAR", "CDLDRAGONFLYDOJI", "CDLGRAVESTONEDOJI", 
    "CDLLONGLINE", "CDLMARUBOZU", "CDLSPINNINGTOP"
]

    
    predictions = {}
    for pattern_name, pattern_indices in patterns.items():
        if any(pattern_name.upper() in pattern for pattern in bullish_patterns):
            movement_prediction = 'Up'
        elif any(pattern_name.upper() in pattern for pattern in bearish_patterns):
            movement_prediction = 'Down'
        elif any(pattern_name.upper() in pattern for pattern in neutral_patterns):
            movement_prediction = 'Neutral'
        else:
            movement_prediction = 'No clear direction'
        
        predictions[pattern_name] = {
            "Indices": pattern_indices.tolist(),
            "Prediction": movement_prediction
        }
    
    return predictions

def main():
    st.title('Live Trading Chart')

    # Sidebar options
    st.sidebar.title('Options')
    ticker_input = st.sidebar.text_input("Enter Ticker Symbol (e.g., AAPL, GOOGL):", "^NSEI")
    period = st.sidebar.selectbox('Select Period:', ['2h', '1d', '5d', '1mo', '3mo'])
    interval = st.sidebar.selectbox('Select Interval:', ['1m', '5m', '15m', '30m', '1h'])
    chart_type = st.sidebar.selectbox('Select Chart Type:', ['Line Chart', 'Candlestick Chart'])
    start_button = st.sidebar.button("Start")

    fig = go.Figure()
    patterns = {}  # Store detected patterns

    if start_button:
        chart = st.plotly_chart(fig, use_container_width=True)
        try:
            while True:
                # Fetch candlestick data
                data = fetch_candlestick_data(ticker_input, period, interval)

                # Clear existing traces
                fig.data = []

                # Plot selected chart type
                if chart_type == 'Line Chart':
                    plot_line_chart(data, fig)
                elif chart_type == 'Candlestick Chart':
                    if not patterns:
                        # Detect candlestick patterns only once
                        patterns = detect_candlestick_patterns(data)

                    # Plot candlestick chart with patterns
                    plot_candlestick(data, fig, patterns)

                    # Display predicted patterns below the graph
                    if patterns:
                        st.write("Detected Patterns:")
                        for pattern_name, pattern_data in patterns.items():
                            st.write(f"Pattern: {pattern_name}, Indices: {', '.join(map(str, pattern_data['Indices']))}, Prediction: {pattern_data['Prediction']}")

                # Update existing chart
                chart.plotly_chart(fig, use_container_width=True)

                # Adjust x-axis range for continuous visualization
                fig.update_xaxes(range=[data.index[-1] - pd.Timedelta(hours=2), data.index[-1]])

                # Zoom functionality
                fig.update_layout(autosize=True, margin=dict(t=20, b=20, l=0, r=0),
                                  xaxis=dict(rangeslider=dict(visible=True), type="date"))

                # Wait for 5 seconds before refreshing
                time.sleep(5)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
