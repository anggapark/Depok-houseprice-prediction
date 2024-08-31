import pathlib
from flask import Flask
from typing import Any, Iterable
from sklearn.preprocessing import OneHotEncoder
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np


app = Flask(__name__)

# Load model
with open(
    "./data/06_models/lr_model.pickle", "rb"
) as f:
    model = pickle.load(f)

# load onehot encoder
with open("./data/05_model_input/encoder.pickle", "rb") as e:
    encoder = pickle.load(e)

# preprocess function
# Assume that encoder is predefined and fitted during training


def preprocess_input(arr: np.array, encoder) -> np.array:
    """Preprocess user input data
    1. Log transform for numeric data
    2. Onehot encoding for non-binary categories
    Args:
        arr (np.array): User input array containing all the features
        encoder: The OneHotEncoder used during training
    Returns:
        np.array: Preprocessed array ready for prediction
    """

    # Convert numeric inputs to float
    numeric_features = arr[:5].astype(float).reshape(1, -1)
    categorical_features = arr[5:8].reshape(
        1, -1
    )  # [subcategories, furnished, location]
    binary_features = (
        arr[8:].astype(float).reshape(1, -1)
    )  # [ac_unit, balcony, yard, security, pool]

    # Log transform for building_size and land_size
    numeric_features[0, 2] = np.log1p(numeric_features[0, 2])  # building_size
    numeric_features[0, 3] = np.log1p(numeric_features[0, 3])  # land_size

    # Onehot encoding for categorical features
    categorical_features_encoded = encoder.transform(categorical_features)

    # Combine all preprocessed features
    preprocessed_arr = np.hstack(
        [numeric_features, categorical_features_encoded, binary_features]
    )
    return preprocessed_arr


def postprocess(log_price: float) -> float:
    """Back-transform log-transformed price prediction

    Args:
        log_price (float): Predicted log-transformed price

    Returns:
        float: actual price
    """
    actual_price = np.expm1(log_price)  # Use expm1 to reverse log1p
    return actual_price


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Get user input from form
    bedroom = request.form.get("bedroom")
    bathroom = request.form.get("bathroom")
    bs = request.form.get("building_size")
    ls = request.form.get("land_size")
    nf = request.form.get("num_floors")
    subcat = request.form.get("subcategories")
    furnished = request.form.get("furnished")
    location = request.form.get("location")
    ac = "1" if request.form.get("ac_unit") == "true" else "0"
    balcony = "1" if request.form.get("balcony") == "true" else "0"
    yard = "1" if request.form.get("yard") == "true" else "0"
    security = "1" if request.form.get("security") == "true" else "0"
    pool = "1" if request.form.get("pool") == "true" else "0"

    # Combine all input data into a numpy array
    input_data = np.array(
        [
            bedroom,
            bathroom,
            bs,
            ls,
            nf,
            subcat,
            furnished,
            location,
            ac,
            balcony,
            yard,
            security,
            pool,
        ]
    )

    # Preprocess the input
    preprocessed_input = preprocess_input(input_data, encoder)

    # Predict the house price (log-transformed)
    log_predicted_price = model.predict(preprocessed_input)[0].item()

    # Postprocess to get the actual price
    predicted_price = "{:,.2f}".format(postprocess(log_predicted_price))

    return render_template(
        "index.html",
        prediction_text=f"The predicted house price is: Rp. {predicted_price}",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
