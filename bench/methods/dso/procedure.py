import click
import json
import os
import sys
import logging
import numpy as np
from dso import DeepSymbolicRegressor

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class DsoProcedure(MethodEvaluator):
    """
    Deep Symbolic Optimization Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)

        if test:
            params = {
                "gp_meld": {
                    "generations": 1,
                    "mutate_tree_max": 2,
                    "p_crossover": 0.5,
                    "p_mutate": 0.5,
                    "parallel_eval": False,
                    "run_gp_meld": False,
                    "tournament_size": 1,
                    "train_n": 1,
                    "verbose": False
                },
                "task": {
                    "task_type" : "regression",
                    "function_set": ["add", "sub", "mul", "div", "sin", "cos", "sqrt"],
                },
                "training": {
                    "n_samples": 2,
                    "batch_size": 1,
                    "epsilon": 0.05,
                    "n_cores_batch": 1,
                    "verbose": False
                }
            }

        else:
            params = {
                "task": {
                    "task_type": "regression",
                    "function_set": ["add", "sub", "mul", "div", "sin", "cos", "sqrt", "exp"],
                },
                "training": {
                    "n_samples": 2000000,
                    "batch_size": 1000,
                    "epsilon": 0.05,
                    "n_cores_batch": -1
                }
            }

        self._method = DeepSymbolicRegressor(params)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x.to_numpy(), train_y.to_numpy())

        yhat = self._method.predict(test_x.to_numpy())
        mse = np.square(yhat - test_y).mean()
        logging.info(f"DSO MSE is: {mse}")
        logging.info(self._method.program_.pretty())
        result = {
            "method": "DSO",
            "mse": mse,
            "equation": self._method.program_.pretty()
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
    method = DsoProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate Deep Symbolic Optimization procedure with data from the path {data_path}.")
        result = {
            "method": f"Deep Symbolic Optimization procedure failed with data from {data_path}",
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
