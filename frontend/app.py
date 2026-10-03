
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

store_establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1900,
    max_value=2026,
    value=2000,
    step=1
)

store_age = st.number_input(
    "Store Age",
    min_value=0,
    value=10,
    step=1
)


# Collect user input for categorical features

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    category_options["Product_Sugar_Content"]
)

product_type = st.selectbox(
    "Product Type",
    category_options["Product_Type"]
)

store_id = st.selectbox(
    "Store ID",
    category_options["Store_Id"]
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

product_category = st.selectbox(
    "Product Category",
    category_options["Product_Category"]
)

product_perishability = st.selectbox(
    "Product Perishability",
    category_options["Product_Perishability"]
)

# Product_Id is retained in the model as a categorical feature.
# Since displaying 8700+ Product IDs is not practical, a valid Product ID
# is automatically selected based on the first two characters, which
# correspond to the selected Product Category.

valid_product_ids = [
    product_id
    for product_id in category_options["Product_Id"]
    if product_id[:2] == product_category
]

if valid_product_ids:
    product_id = valid_product_ids[0]
else:
    product_id = None
    st.error("No valid Product ID found for the selected Product Category.")

# Convert user input into a DataFrame

input_data = pd.DataFrame([{

    "Product_Weight": product_weight,

    "Product_Allocated_Area": product_allocated_area,

    "Product_MRP": product_mrp,

    "Store_Establishment_Year": store_establishment_year,

    "Store_Age": store_age,

    "Product_Id": product_id,

    "Product_Sugar_Content": product_sugar_content,

    "Product_Type": product_type,

    "Store_Id": store_id,

    "Store_Size": store_size,

    "Store_Location_City_Type": store_location_city_type,

    "Store_Type": store_type,

    "Product_Category": product_category,

    "Product_Perishability": product_perishability

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
