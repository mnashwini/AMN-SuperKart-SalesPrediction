
import streamlit as st
import pandas as pd
import requests
import json

# Base URL of the Flask backend
BACKEND_URL = "http://172.18.0.1:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")


# Section for online prediction
st.subheader("Online Prediction")

# Load categorical feature options
with open("category_options.json", "r") as file:
    category_options = json.load(file)

# Collect user input for numerical features

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=10.0
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=100.0
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=100.0
)

store_age_years = st.number_input(
    "Store Age Years",
    min_value=0,
    value=10,
    step=1
)


# Collect user input for categorical features

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    category_options["Product_Sugar_Content"]
)

store_size = st.selectbox(
    "Store Size",
    category_options["Store_Size"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    category_options["Store_Location_City_Type"]
)

store_type = st.selectbox(
    "Store Type",
    category_options["Store_Type"]
)

product_id_char = st.selectbox(
    "Product ID Char",
    category_options["Product_Id_char"]
)

product_type_category = st.selectbox(
    "Product Type Category",
    category_options["Product_Type_Category"]
)


# Convert user input into a DataFrame

input_data = pd.DataFrame([{

    "Product_Weight": product_weight,

    "Product_Allocated_Area": product_allocated_area,

    "Product_MRP": product_mrp,

    "Store_Age_Years": store_age_years,

    "Product_Sugar_Content": product_sugar_content,

    "Store_Size": store_size,

    "Store_Location_City_Type": store_location_city_type,

    "Store_Type": store_type,

    "Product_Id_char": product_id_char,

    "Product_Type_Category": product_type_category

}])


# Make prediction when the "Predict" button is clicked

if st.button("Predict", type="primary"):

    response = requests.post(
        f"{BACKEND_URL}/v1/sales",
        json=input_data.to_dict(orient="records")[0]
    )


    # Display the prediction returned by the Flask API

    if response.status_code == 200:

        prediction = response.json()[
            "Predicted Product Store Sales Total"
        ]

        st.success(
            f"Predicted Product Store Sales Total: {prediction}"
        )

    else:

        st.error("Unable to connect to the prediction API.")


# Section for batch prediction

st.subheader("Batch Prediction")


# Allow users to upload a CSV file for batch prediction

uploaded_file = st.file_uploader(
    "Upload CSV file for batch prediction",
    type=["csv"]
)


# Make batch prediction when the "Predict Batch" button is clicked

if uploaded_file is not None:

    if st.button("Predict Batch", type="primary"):

        response = requests.post(
            f"{BACKEND_URL}/v1/salesbatch",
            files={"file": uploaded_file}
        )


        if response.status_code == 200:

            predictions = response.json()

            st.success("Batch predictions completed!")

            st.write(predictions)

        else:

            st.error("Unable to connect to the prediction API.")
