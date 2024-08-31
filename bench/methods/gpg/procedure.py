import click
import json
import os
import sys
import logging
import numpy as np
from pygpg.sk import GPGRegressor

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class GpgProcedure(MethodEvaluator):
    """
    gpg Procedure for benchmark methods.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)

        if test:
            params = {
                "e": 100,  # 50,000 evaluations limit for search
                "t": 60,  # time limit,
                "g": 5,  # no generation limit,
                "d": 2,  # maximum tree depth
                "finetune": True,  # whether to fine-tune the coefficients after the search
                "finetune_max_evals": 10,  # 10,000 evaluations limit for fine-tuning
                "verbose": True  # print progress
            }
        else:
            params = {
                "e": 200_000,                   # 50,000 evaluations limit for search
                "t": 7200,                     # time limit,
                "g": -1,                       # no generation limit,
                "d": 6,                        # maximum tree depth
                "tour": 5,                     # tournament size
                "pop": 4096,                   # population size
                "finetune": True,              # whether to fine-tune the coefficients after the search
                "finetune_max_evals": 10_000,  # 10,000 evaluations limit for fine-tuning
                "verbose": True,               # print progress
                "fset": '+,-,*,/,log,sqrt,sin,cos' # operators to use
            }

        self._method = GPGRegressor(**params)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x, train_y)

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()
        model_expression = str(self._method.model)
        logging.info(f"gpg MSE is: {mse}")
        logging.info(model_expression)
        result = {
            "method": "gpg",
            "mse": mse,
            "equation": model_expression
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
    method = GpgProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate Template procedure with data from the path {data_path}.")
        result = {
            "method": f"gpg procedure failed with data from {data_path}",
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
