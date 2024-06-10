import click
import json
import os
import sys
import logging
import numpy as np
from sklearn.linear_model import LinearRegression

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class TemplateProcedure(MethodEvaluator):
    """
    Template Procedure for benchmark methods.
    Each method must implement a procedure function for benchmarking methods.
    There should also be a test mode to run a simplified procedure for testing.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)

        if test:
            params = {
                "fit_intercept": False
            }
        else:
            params = {
                "fit_intercept": True
            }

        self._method = LinearRegression(**params)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x, train_y)

        # Reconstructing expression up to a constant
        expression = ""
        for i, value in enumerate(list(self._method.coef_)):
            expression += f"{value}x{i}+"

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()
        logging.info(f"Template MSE is: {mse}")
        logging.info(expression[:-1])
        result = {
            "method": "Template",
            "mse": mse,
            "equation": expression[:-1]
        }
        return result


@click.command()
@click.option(
    '--data_path',
    type=click.Path(exists=True),
    help='Path to a csv dataset containing a column called "target" as result and other columns as input parameters'
)
@click.option(
    '--verbose',
    type=int,
    default=2,
    help='Set the level of verbosity. 1 is the highest level and 5 is the lowest.'
)
@click.option(
    '--test',
    type=bool,
    default=False,
    help='If true, use test parameters'
)
def main(data_path: str, verbose: int, test: bool) -> None:
    method = TemplateProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate Template procedure with data from the path {data_path}.")
        result = {
            "method": f"Template procedure failed with data from {data_path}",
            "mse": 0,
            "equation": "No equation obtained"
        }
    with open(f"{PATH}/result.json", "w") as result_file:
        json.dump(result, result_file)


if __name__ == "__main__":
    """
    This class runs the benchmark method and evaluate a given dataset.
    The evaluation is performed by the evaluate method of the superclass MethodEvaluator.

    The function takes the following arguments:
        data_path (str):      The path of the dataset to be evaluated.
        verbose (int):        Set the log level.
        test (bool):          Enable test hyperparameters.
    """
    main()
