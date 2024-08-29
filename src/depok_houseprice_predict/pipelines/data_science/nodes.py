"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.3
"""

import logging
from typing import Dict, Tuple, Any
import pandas as pd

# from sklearn.pipeline import Pipeline
# from sklearn.compose import ColumnTransformer

from sklearn.linear_model import RANSACRegressor, LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    root_mean_squared_error,
    r2_score,
)


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


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Trains the linear regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.

    Returns:
        Trained model.
    """
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return regressor


def evaluate_model(
    regressor: LinearRegression, X_test: pd.DataFrame, y_test: pd.Series
):
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = regressor.predict(X_test)
    score = root_mean_squared_error(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has a RMSE of %.3f on test data.", score)
    # logger.info("Model has a coefficient R^2 of %.3f on test data.", score)
