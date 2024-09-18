import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

# Title
st.title("Stock Price Predictor App")

# Get stock ID
stock = st.text_input("Enter the Stock ID", "GOOG")

# Fetch stock data
end = datetime.now()
start = datetime(end.year - 20, end.month, end.day)
google_data = yf.download(stock, start, end)

# Check if stock data is fetched
if google_data.empty:
    st.error("No data found for this stock. Please try another.")
else:
    # Display stock data
    st.subheader("Stock Data")
    st.write(google_data)

    # Try loading the model
    try:
        model = load_model(r"E:\CS50P\Latest_stock_price_model.keras")
    except Exception as e:
        st.error(f"Error loading model: {e}. Please check the file path or file format.")
    
    # Continue with plotting only if the model is loaded
    if 'model' in locals():
        splitting_len = int(len(google_data) * 0.7)
        x_test = pd.DataFrame(google_data.Close[splitting_len:])

        # Function to plot data
        def plot_graph(figsize, values, full_data, extra_data=0, extra_dataset=None):
            fig = plt.figure(figsize=figsize)
            plt.plot(values, 'orange')
            plt.plot(full_data.Close, 'b')
            if extra_data:
                plt.plot(extra_dataset)
            return fig

        # Add moving averages and plot graphs
        google_data['MA_for_250_days'] = google_data.Close.rolling(250).mean()
        google_data['MA_for_200_days'] = google_data.Close.rolling(200).mean()
        google_data['MA_for_100_days'] = google_data.Close.rolling(100).mean()

        st.subheader('Original Close Price and MA for 250 days')
        st.pyplot(plot_graph((15, 6), google_data['MA_for_250_days'], google_data))

        st.subheader('Original Close Price and MA for 200 days')
        st.pyplot(plot_graph((15, 6), google_data['MA_for_200_days'], google_data))

        st.subheader('Original Close Price and MA for 100 days')
        st.pyplot(plot_graph((15, 6), google_data['MA_for_100_days'], google_data))

        st.subheader('Original Close Price and MA for 100 days and MA for 250 days')
        st.pyplot(plot_graph((15, 6), google_data['MA_for_100_days'], google_data, 1, google_data['MA_for_250_days']))

        # Scale and predict stock prices
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(x_test[['Close']])

        x_data = []
        y_data = []

        for i in range(100, len(scaled_data)):
            x_data.append(scaled_data[i-100:i])
            y_data.append(scaled_data[i])

        x_data, y_data = np.array(x_data), np.array(y_data)

        predictions = model.predict(x_data)

        # Inverse scaling of the predictions
        inv_pre = scaler.inverse_transform(predictions)
        inv_y_test = scaler.inverse_transform(y_data)

        # Create a DataFrame for plotting the predicted vs actual data
        ploting_data = pd.DataFrame({
            'original_test_data': inv_y_test.reshape(-1),
            'predictions': inv_pre.reshape(-1)
        }, index=google_data.index[splitting_len+100:])

        st.subheader("Original values vs Predicted values")
        st.write(ploting_data)

        # Plot original vs predicted close prices
        st.subheader('Original Close Price vs Predicted Close price')
        fig = plt.figure(figsize=(15, 6))
        plt.plot(pd.concat([google_data.Close[:splitting_len+100], ploting_data], axis=0))
        plt.legend(["Data- not used", "Original Test data", "Predicted Test data"])
        st.pyplot(fig)
