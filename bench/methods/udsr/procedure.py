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


class UdsrProcedure(MethodEvaluator):
    """
    Unified Deep Symbolic Regression Procedure.

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
                    "function_set": ["add", "sub", "mul", "div", "sin", "cos", "sqrt", "poly"],
                    "poly_optimizer_params": {
                        "degree": 3,
                        "coef_tol": 1e-6,
                        "regressor": "dso_least_squares",
                        "regressor_params": {}
                    }
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
                    "metric": "inv_nrmse",
                    "metric_params": [1.0],
                    "threshold": 1e-12,
                    "function_set": ["add", "sub", "mul", "div", "sin", "cos", "sqrt", "exp", "poly"],
                    "poly_optimizer_params": {
                        "degree": 5,
                        "coef_tol": 1e-5,
                        "regressor": "dso_least_squares",
                        "regressor_params": {
                        "n_max_terms": 10,
                        }
                    }
                },
                "training": {
                    "n_samples": 2000000,
                    "batch_size": 1000,
                    "epsilon": 0.05,
                    "alpha": 0.5,
                    "n_cores_batch": -1
                },
                "prior": {
                    "length": {
                        "min_": 1,
                        "max_": 10,
                        "on": True
                    },
                    "no_inputs": {
                        "on": False
                    },
                    "const": {
                        "on": False
                    },
                    "trig": {
                        "on": False
                    },
                    "uniform_arity": {
                        "on": False
                    },
                    "soft_length": {
                        "loc": 5,
                        "scale": 5,
                        "on": True
                    },
                },
                "logging": {
                    "save_pareto_front": False,
                },
                "policy": {
                    "policy_type": "rnn",
                    "max_length": 64,
                    "cell": "lstm",
                    "num_layers": 2,
                    "num_units": 64,
                    "initializer": "zeros"
                },
                "policy_optimizer": {
                    "policy_optimizer_type": "pg",
                    "learning_rate": 0.00005,
                    "optimizer": "adam",
                    "entropy_weight": 0.01,
                    "entropy_gamma": 1.0
                },

            }

        self._method = DeepSymbolicRegressor(params)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x.to_numpy(), train_y.to_numpy())

        yhat = self._method.predict(test_x.to_numpy())
        mse = np.square(yhat - test_y).mean()
        logging.info(f"uDSR MSE is: {mse}")
        logging.info(self._method.program_.pretty())
        result = {
            "method": "uDSR",
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
    method = UdsrProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate UDSR procedure with data from the path {data_path}.")
        result = {
            "method": f"UDSR procedure failed with data from {data_path}",
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
