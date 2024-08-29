"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 0.19.3
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import split_dataset, train_model, evaluate_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_dataset,
                inputs="preprocessed_housedata",
                outputs=[
                    "X_train",
                    "y_train",
                    "X_test",
                    "y_test",
                ],
                name="split_dataset",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="regressor",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["regressor", "X_test", "y_test"],
                outputs=None,
                name="evaluate_model_node",
            ),
        ]
    )
