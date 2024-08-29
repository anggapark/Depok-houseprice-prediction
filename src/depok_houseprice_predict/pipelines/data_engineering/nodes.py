"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.3
"""

import re
from typing import Any, Dict, List
import pandas as pd
import numpy as np
from math import ceil
from scipy.stats import skew
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Change datatype while ignoring missing value

    Args:
        df (pd.DataFrame): all numeric features of data

    Returns:
        pd.DataFrame: fixed data types numeric features
    """

    for column in ["bedrooms", "bathrooms", "num_floors", "price"]:
        if not pd.api.types.is_numeric_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], errors="coerce").astype(
                int, errors="ignore"
            )

    for column in ["building_size", "land_size"]:
        if not pd.api.types.is_numeric_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], errors="coerce").astype(
                float, errors="ignore"
            )

    return df


def parse_subcategories(x: pd.Series) -> pd.Series:
    """parse subcategories columns and pick only second element of list
    example:
        ["house","single-family-house"] to "single-family-house"


    Args:
        x (pd.Series): original subcategories column

    Returns:
        pd.Series: parse result of subcategories
    """
    x = x.apply(
        lambda x: x.replace("[", "").replace("]", "").replace('"', "").split(",")[1]
    )
    return x


def prep_location(x: pd.Series) -> pd.Series:
    """parse parent_url column to get house location
    example:
        https://www.lamudi.co.id/west-java/depok/cimanggis/house/buy/ to "cimanggis"
        https://www.lamudi.co.id/west-java/depok/sawangan-1/house/buy/ to "sawangan"

    Args:
        x (pd.Series): page url features of data

    Returns:
        pd.Series: location parsed from page url
    """
    x = x.apply(lambda x: re.sub("-?\d+", "", x.split("/")[5]).replace("-", " "))
    return x


def calculate_floors(
    floors: pd.Series, building_land_div: pd.Series, url: pd.Series
) -> pd.Series:
    """calculate and fix num_floors by either from url or result of division of building_size and land_size

    Args:
        floors (pd.Series): number of floor values
        building_land_div (pd.Series): division of building_size and land_size
        url (pd.Series): webpage url of house

    Returns:
        pd.Series: Results of number of floor
    """
    floor_pattern = "(\\d+).?(lantai|lt)"
    floors_by_pattern = url.apply(
        lambda x: (
            int(re.search(floor_pattern, x)[1]) if re.search(floor_pattern, x) else 0
        )
    )

    floors_by_size = np.vectorize(ceil)(building_land_div)

    # Use conditional logic to determine floors based on pattern and size constraints
    floors = np.where(
        (floors_by_pattern != 0) & (floors_by_pattern < 5),
        floors_by_pattern,
        floors_by_size,
    )

    # No need to drop columns as they weren't created directly
    return floors.astype(int)


def prep_furnished(x: pd.Series) -> pd.Series:
    """Map furnished values to either yes, no, or semi

    Args:
        x (pd.Series): furnished feature of data

    Returns:
        pd.Series: Mapping result of furnished values
    """
    furnished_map = {"11": "yes", "123": "no", "124": "semi"}
    x = x.map(furnished_map)
    return x.fillna("no")


def prep_facility(df: pd.DataFrame) -> pd.DataFrame:
    """preprocessed facility columns

    Args:
        df (pd.DataFrame): house facility of dataset

    Returns:
        pd.DataFrame: 'yes' if house has feature and 'no' if house does not have feature
    """
    facility = ["ac_unit", "balcony", "yard", "security", "pool"]

    return df[facility] == "yes"


def log_transformation(df: pd.DataFrame) -> pd.DataFrame:
    """address the issue of skewed features using log transformation

    Args:
        df (pd.DataFrame): extremely skewed features of data

    Returns:
        pd.DataFrame: log result of skewed data
    """
    cols = df[["building_size", "land_size", "price"]]
    skewed_train = cols.apply(lambda x: skew(x.dropna()))
    skewed_train = skewed_train[skewed_train > 0.75]
    df[skewed_train.index] = np.log1p(df[skewed_train.index])

    return df


def onehot_encoding(df: pd.DataFrame) -> pd.DataFrame:
    """convert multiple categorical values to numeric using one hot encoding

    Args:
        df (pd.DataFrame): original dataframe

    Returns:
        pd.DataFrame: dataframe with encoded categorical values
    """
    # Extract categorical columns from the dataframe
    categorical_columns = ["subcategories", "furnished", "location"]
    # Initialize OneHotEncoder
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    # Apply one-hot encoding to the categorical columns
    one_hot_encoded = encoder.fit_transform(df[categorical_columns])
    # Create a DataFrame with the one-hot encoded columns
    one_hot_df = pd.DataFrame(
        one_hot_encoded, columns=encoder.get_feature_names_out(categorical_columns)
    )  # get_feature_names_out() to get the column names for the encoded data

    # Concatenate the one-hot encoded dataframe with the original dataframe
    df_encoded = pd.concat([df, one_hot_df], axis=1)
    # Drop the original categorical columns
    df_encoded = df_encoded.drop(categorical_columns, axis=1)
    return df_encoded


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process the data for model training

    Args:
        df (pd.DataFrame): dataset used to build machine learning model

    Returns:
        pd.DataFrame: preprocessed dataset
    """
    # "bedrooms", "bathrooms", "num_floors", "price", "building_size", "land_size"
    df = convert_dtypes(df)
    # subcategories
    df["subcategories"] = parse_subcategories(df["subcategories"])
    # locations
    df["location"] = prep_location(df["parent_url"])
    # furnished
    df["furnished"] = prep_furnished(df["furnished"])
    # house facility
    facility = ["ac_unit", "balcony", "yard", "security", "pool"]
    df[facility] = prep_facility(df[facility])
    # num_floors
    # df["building_land_ratio"] = df["building_size"] / df["land_size"]
    df["num_floors"] = calculate_floors(
        df["num_floors"], df["building_size"] / df["land_size"], df["page_url"]
    )
    df = log_transformation(df)
    df = onehot_encoding(df)

    return df


def train_test_split(prep_df: pd.DataFrame):
    """Split processed data into train and test sets

    Args:
        prep_df (pd.DataFrame): DataFrame containing the processed house dataset

    Returns:
        Tuple: train data, train labels, test data, and test labels
    """
    train_df = prep_df.iloc[:6489,]
    test_df = prep_df.iloc[6489:,]

    X_train = train_df.drop(
        columns=["price", "categories", "geo_point", "page_url", "parent_url"], axis=1
    )
    y_train = train_df["price"]

    X_test = test_df.drop(
        columns=["price", "categories", "geo_point", "page_url", "parent_url"], axis=1
    )
    y_test = test_df["price"]

    return (
        X_train,
        y_train,
        X_test,
        y_test,
    )
