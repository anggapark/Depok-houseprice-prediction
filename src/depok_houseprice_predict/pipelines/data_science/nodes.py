"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.3
"""

import logging
from typing import Dict, Tuple, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error

# from sklearn.pipeline import Pipeline
# from sklearn.compose import ColumnTransformer
# from sklearn.linear_model import RANSACRegressor, LinearRegression, Ridge, Lasso


def split_dataset(data: pd.DataFrame) -> Tuple:
    """Split processed data into train and test sets

    Args:
        prep_df (pd.DataFrame): DataFrame containing the processed house dataset

    Returns:
        Tuple: train data, train labels, test data, and test labels
    """
    X = data.drop(
        columns=["price", "categories", "geo_point", "page_url", "parent_url"], axis=1
    )
    y = data["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    return (
        X_train,
        y_train,
        X_test,
        y_test,
    )


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestRegressor:
    """Trains the linear regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.

    Returns:
        Trained model.
    """
    regressor = RandomForestRegressor()
    regressor.fit(X_train, np.ravel(y_train))
    return regressor


def predict(regressor: RandomForestRegressor, X_test: pd.DataFrame) -> pd.Series:
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = regressor.predict(X_test)
    return y_pred


def evaluate_model(y_pred: pd.Series, y_test: pd.Series):
    """Evaluate predicted model with ground truth label

    Args:
        y_pred (pd.Series): Predicted result from trained model
        y_test (pd.Series): Ground truth label

    Returns:
        score: _description_
    """
    score = root_mean_squared_error(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has a RMSE of %.3f on test data.", score)

    return score
