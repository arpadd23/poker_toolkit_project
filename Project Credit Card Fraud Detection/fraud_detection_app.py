import streamlit as st
import numpy as np
import joblib

# Load the pre-trained model
model = joblib.load('E:/Project Credit Card Fraud Detection Using Machine Learnin 2024 09/credit_card_model.pkl')


# Define the input features for the model (there are 29 features to input)
st.title("Credit Card Fraud Detection")

# Create input fields for each of the 29 features
V1 = st.number_input("V1", value=0.0)
V2 = st.number_input("V2", value=0.0)
V3 = st.number_input("V3", value=0.0)
V4 = st.number_input("V4", value=0.0)
V5 = st.number_input("V5", value=0.0)
V6 = st.number_input("V6", value=0.0)
V7 = st.number_input("V7", value=0.0)
V8 = st.number_input("V8", value=0.0)
V9 = st.number_input("V9", value=0.0)
V10 = st.number_input("V10", value=0.0)
V11 = st.number_input("V11", value=0.0)
V12 = st.number_input("V12", value=0.0)
V13 = st.number_input("V13", value=0.0)
V14 = st.number_input("V14", value=0.0)
V15 = st.number_input("V15", value=0.0)
V16 = st.number_input("V16", value=0.0)
V17 = st.number_input("V17", value=0.0)
V18 = st.number_input("V18", value=0.0)
V19 = st.number_input("V19", value=0.0)
V20 = st.number_input("V20", value=0.0)
V21 = st.number_input("V21", value=0.0)
V22 = st.number_input("V22", value=0.0)
V23 = st.number_input("V23", value=0.0)
V24 = st.number_input("V24", value=0.0)
V25 = st.number_input("V25", value=0.0)
V26 = st.number_input("V26", value=0.0)
V27 = st.number_input("V27", value=0.0)
V28 = st.number_input("V28", value=0.0)
Amount = st.number_input("Amount", value=0.0)

# Predict when the button is pressed
if st.button("Predict"):
    # Prepare the input array
    input_data = np.array([[V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount]])

    # Make a prediction
    prediction = model.predict(input_data)

    # Display the result
    if prediction[0] == 0:
        st.success("Normal Transaction")
    else:
        st.error("Fraudulent Transaction")
