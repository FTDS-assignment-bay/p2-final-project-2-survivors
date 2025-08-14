import pandas as pd
import numpy as np

import pickle as pkl
import streamlit as st

try:
    with open('src/best_delivery_delay_model_xgb.pkl', 'rb') as file:
        model = pkl.load(file)
except FileNotFoundError:
    st.error("Model file not found. Please check the path and ensure the file exists.")
    model = None


def run():
    # title
    st.title("Delivery Delay Prediction")
    st.markdown('---')

    # section data
    df = pd.read_csv('C:\\Users\\User\\p2-final_project\\p2-final-project-2-survivors\\delivery_predictor\\src\\cleaned_data.csv')

    # input form
    with st.form(key='delivery_form'):
        warehouse_block = st.selectbox("Warehouse Block", df["warehouse_block"].unique())
        mode_of_shipment = st.selectbox("Mode of Shipment", df["mode_of_shipment"].unique())
        customer_care_calls = st.number_input("Customer Care Calls", min_value=0, value=0)
        customer_rating = st.number_input("Customer Rating", min_value=0, max_value=10, value=5)
        cost_of_the_product = st.number_input("Cost of the Product", min_value=0.0, value=0.0)
        prior_purchases = st.number_input("Prior Purchases", min_value=0, value=0)
        product_importance = st.selectbox("Product Importance", df["product_importance"].unique())
        gender = st.selectbox("Gender", df["gender"].unique())
        discount_offered = st.number_input("Discount (%)", min_value=0, max_value=100, value=0)
        weight_in_gms = st.number_input("Weight (g)", min_value=0, value=0)
        
        submit_button = st.form_submit_button(label='Predict Delivery Delay')

    if submit_button:
        # make prediction
        input_data = pd.DataFrame({
            "warehouse_block": [warehouse_block],
            "mode_of_shipment": [mode_of_shipment],
            "customer_care_calls": [customer_care_calls],
            "customer_rating": [customer_rating],
            "cost_of_the_product": [cost_of_the_product],
            "prior_purchases": [prior_purchases],
            "product_importance": [product_importance],
            "gender": [gender],
            "discount_offered": [discount_offered],
            "weight_in_gms": [weight_in_gms]
            
        })

        prediction = model.predict(input_data)
        st.write(f"Predicted Delivery Delay: {prediction[0]}")

if __name__ == "__main__":
    run()