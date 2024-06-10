import click
import json
import os
import sys
import logging
import numpy as np
from ffx import FFXRegressor

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class FfxProcedure(MethodEvaluator):
    """
    Fast Function Extraction Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
    """
    def __init__(self, verbose=2):
        super().__init__(verbose)
        self._method = FFXRegressor()

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x, train_y)

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()
        expression = self._method.model_.str2().replace('^', '**')
        logging.info(f"FFX MSE is: {mse}")
        logging.info(expression)
        result = {
            "method": "FFX",
            "mse": mse,
            "equation": expression
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
    method = FfxProcedure(verbose)
    result = method.evaluate(data_path)
    if test:
        logging.error("Fast Function Extraction has no test hyperparameters")
    if result == 1:
        logging.error(f"Failed to evaluate Fast Function Extraction procedure with data from the path {data_path}.")
        result = {
            "method": f"Fast Function Extraction procedure failed with data from {data_path}",
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
