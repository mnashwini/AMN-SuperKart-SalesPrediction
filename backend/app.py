# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_predictor_api = Flask("SuperKart Sales Prediction API")


# Load the trained machine learning model
model = joblib.load("superkart_model.joblib")


# Define a route for the home page (GET request)
@superkart_sales_predictor_api.get('/')
def home():

    """
    This function handles GET requests to the root URL ('/').
    It returns a simple welcome message.
    """

    return "Welcome to the SuperKart Sales Prediction API!"


# Define an endpoint for single prediction (POST request)
@superkart_sales_predictor_api.post('/v1/sales')
def predict_sales():

    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing product and store details
    and returns the predicted total store sales.
    """

    # Get the JSON data from the request body
    product_data = request.get_json()


    # Extract the required features from the JSON data
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Product_Id_char': product_data['Product_Id_char'],
        'Product_Type_Category': product_data['Product_Type_Category']
    }


    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])


    # Make the prediction
    predicted_sales = model.predict(input_data)[0]


    # Convert the prediction to a Python float and round it
    predicted_sales = round(float(predicted_sales), 2)


    # Return the prediction as a JSON response
    return jsonify({
        'Predicted Product Store Sales Total': predicted_sales
    })


# Define an endpoint for batch prediction (POST request)
@superkart_sales_predictor_api.post('/v1/salesbatch')
def predict_sales_batch():

    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing product and store details
    and returns predicted sales for all records.
    """

    # Get the uploaded CSV file from the request
    file = request.files['file']


    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)


    # Make predictions for all records
    predicted_sales = model.predict(input_data).tolist()


    # Convert predictions to Python floats and round them
    predicted_sales = [
        round(float(sales), 2)
        for sales in predicted_sales
    ]


    # Create a dictionary containing the predictions
    output_dict = dict(
        zip(
            range(1, len(predicted_sales) + 1),
            predicted_sales
        )
    )


    # Return the predictions as a JSON response
    return output_dict


# Run the Flask application in debug mode
# when this script is executed directly
if __name__ == '__main__':

    superkart_sales_predictor_api.run(debug=True)
