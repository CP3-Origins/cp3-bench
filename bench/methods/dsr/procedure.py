import click
import json
import os
import sys
import logging
import numpy as np
from dsr import DeepSymbolicRegressor

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class DsrProcedure(MethodEvaluator):
    """
    Deep Symbolic Regression (DSR) Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)

        if test:
            params = {
                "task": {
                    "name": "cp3-bench",
                    "task_type": "regression",
                    "function_set": ["add", "sub", "mul", "div", "sin", "cos", "sqrt"],
                },
                "prior": {
                    "length": {"min_": 4, "max_": 30},
                    "repeat": {"tokens": "const", "max_": 3},
                    "inverse": {},
                    "trig": {},
                    "const": {}
                },
                "training": {
                    "logdir": "./log",
                    "n_epochs": None,
                    "n_samples": 20,
                    "batch_size": 1,
                    "complexity": "length",
                    "complexity_weight": 0.0,
                    "const_optimizer": "scipy",
                    "const_params": {},
                    "alpha": 0.5,
                    "epsilon": 0.05,
                    "verbose": True,
                    "baseline": "R_e",
                    "b_jumpstart": False,
                    "n_cores_batch": 1,
                    "summary": False,
                    "debug": 0,
                    "save_all_r": False,
                    "early_stopping": True,
                    "pareto_front": False,
                    "hof": 100
                },
                "controller": {
                    "cell": "lstm",
                    "num_layers": 1,
                    "num_units": 32,
                    "initializer": "zeros",
                    "embedding": False,
                    "embedding_size": 8,
                    "optimizer": "adam",
                    "learning_rate": 0.0005,
                    "observe_action": False,
                    "observe_parent": True,
                    "observe_sibling": True,
                    "entropy_weight": 0.005,
                    "ppo": False,
                    "ppo_clip_ratio": 0.2,
                    "ppo_n_iters": 10,
                    "ppo_n_mb": 4,
                    "pqt": False,
                    "pqt_k": 10,
                    "pqt_batch_size": 1,
                    "pqt_weight": 200.0,
                    "pqt_use_pg": False,
                    "max_length": 30
                },
                "gp": {
                    "population_size": 5,
                    "generations": None,
                    "n_samples": 20,
                    "tournament_size": 2,
                    "metric": "nmse",
                    "const_range": [
                        -1.0,
                        1.0
                    ],
                    "p_crossover": 0.95,
                    "p_mutate": 0.03,
                    "seed": 0,
                    "early_stopping": True,
                    "pareto_front": False,
                    "threshold": 1e-12,
                    "verbose": False,
                    "protected": True,
                    "constrain_const": True,
                    "constrain_trig": True,
                    "constrain_inv": True,
                    "constrain_min_len": True,
                    "constrain_max_len": True,
                    "constrain_num_const": True,
                    "min_length": 4,
                    "max_length": 10,
                    "max_const": 3
                }
            }

        else:
            params = {
                "task": {
                    "name": "cp3-bench",
                    "task_type": "regression",
                    "function_set": ["add", "sub", "mul", "div", "sin", "cos", "sqrt", "exp"],
                },
                "prior": {
                    "length": {"min_": 4, "max_": 25},
                    "repeat": {"tokens": "const", "max_": 3},
                    "inverse": {},
                    "trig": {},
                    "const": {}
                },
                "training": {
                    "logdir": "./log",
                    "n_epochs": None,
                    "n_samples": 5000000,
                    "batch_size": 1000,
                    "complexity": "length",
                    "complexity_weight": 0.0,
                    "const_optimizer": "scipy",
                    "const_params": {},
                    "alpha": 0.5,
                    "epsilon": 0.05,
                    "verbose": True,
                    "baseline": "R_e",
                    "b_jumpstart": False,
                    "n_cores_batch": -1,
                    "summary": False,
                    "debug": 0,
                    "save_all_r": False,
                    "early_stopping": True,
                    "pareto_front": False,
                    "hof": 100
               },
                "controller": {
                    "cell": "lstm",
                    "num_layers": 2,
                    "num_units": 64,
                    "initializer": "zeros",
                    "embedding": False,
                    "embedding_size": 8,
                    "optimizer": "adam",
                    "learning_rate": 0.0005,
                    "observe_action": False,
                    "observe_parent": True,
                    "observe_sibling": True,
                    "entropy_weight": 0.005,
                    "ppo": False,
                    "ppo_clip_ratio": 0.2,
                    "ppo_n_iters": 10,
                    "ppo_n_mb": 4,
                    "pqt": False,
                    "pqt_k": 10,
                    "pqt_batch_size": 1,
                    "pqt_weight": 200.0,
                    "pqt_use_pg": False,
                    "max_length": 30
                },
                "gp": {
                    "population_size": 1000,
                    "generations": None,
                    "n_samples": 2000000,
                    "tournament_size": 2,
                    "metric": "nmse",
                    "const_range": [
                        -1.0,
                        1.0
                    ],
                    "p_crossover": 0.95,
                    "p_mutate": 0.03,
                    "seed": 0,
                    "early_stopping": True,
                    "pareto_front": False,
                    "threshold": 1e-12,
                    "verbose": False,
                    "protected": True,
                    "constrain_const": True,
                    "constrain_trig": True,
                    "constrain_inv": True,
                    "constrain_min_len": True,
                    "constrain_max_len": True,
                    "constrain_num_const": True,
                    "min_length": 4,
                    "max_length": 30,
                    "max_const": 3
                }
            }

        self._method = DeepSymbolicRegressor(params)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x.to_numpy(), train_y.to_numpy())

        yhat = self._method.predict(test_x.to_numpy())
        mse = np.square(yhat - test_y).mean()
        logging.info(f"DSR MSE is: {mse}")
        logging.info(self._method.program_.pretty())
        result = {
            "method": "DSR",
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
    method = DsrProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(
            f"Failed to evaluate Deep Symbolic Regression procedure with data from the path {data_path}."
        )
        result = {
            "method": f"Deep Symbolic Regression procedure failed with data from {data_path}",
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
