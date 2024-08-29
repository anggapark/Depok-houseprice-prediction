"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import preprocess_data, train_test_split


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_data,
                inputs="housedata",
                outputs="preprocessed_housedata",
                name="preprocess_data",
            ),
            node(
                func=train_test_split,
                inputs="preprocessed_housedata",
                outputs=[
                    "X_train",
                    "y_train",
                    "X_test",
                    "y_test",
                ],
                name="train_test_split",
            ),
        ]
    )
