import click
import json
import os
import sys
import logging
import sympy
import numpy as np
from pysr import PySRRegressor

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class PysrProcedure(MethodEvaluator):
    """
    PySR Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)
        if test:
            params = {
                "niterations": 2,
                "binary_operators": ["*","+","-"],
                "unary_operators": [
                    "cos",
                ],
                "loss": "loss(prediction, target) = (prediction - target)^2",
                # ^ Custom loss function (julia syntax)
            }
        else:
            params = {
                "populations": 30,
                # ^ 2 populations per core, so one is always running.
                "population_size": 200,
                # ^ Slightly larger populations, for greater diversity.
                "ncyclesperiteration": 2000,
                # ^ Generations between migrations.
                "niterations": 500,
                "batch_size": 100,
                "early_stop_condition": (
                    "stop_if(loss, complexity) = loss < 1e-6 && complexity < 8"
                    # Stop early if we find a good and simple equation
                ),
                "timeout_in_seconds": 60 * 60 * 6,
                # ^ Alternatively, stop after 6 hours have passed.
                "maxsize": 20,
                # ^ Allow greater complexity.
                "maxdepth": 7,
                # ^ But, avoid deep nesting.
                "binary_operators": ["*", "+", "-", "/"],
                "unary_operators": ["square", "cube", "exp", "cos", "sin"],
                "constraints": {
                    "/": (-1, 9),
                    "square": 3,
                    "cube": 2,
                    "cos": 3,
                    "sin": 3,
                    "exp": 2,
                },
                # ^ Limit the complexity within each argument.
                # "inv": (-1, 9) states that the numerator has no constraint,
                # but the denominator has a max complexity of 9.
                # "exp": 9 simply states that `exp` can only have
                # an expression of complexity 9 as input.
                "nested_constraints": {
                    "square": {"square": 1, "cube": 1, "exp": 0},
                    "cube": {"square": 1, "cube": 1, "exp": 0},
                    "exp": {"square": 1, "cube": 1, "exp": 0},
                },
                # ^ Nesting constraints on operators. For example,
                # "square(exp(x))" is not allowed, since "square": {"exp": 0}.
                "complexity_of_operators": {"/": 3, "exp": 3},
                # ^ Custom complexity of particular operators.
                "complexity_of_constants": 4,
                # ^ Punish constants more than variables
                "select_k_features": 4,
                # ^ Train on only the 4 most important features
                "progress": True,
                # ^ Can set to false if printing to a file.
                "weight_randomize": 0.1,
                # ^ Randomize the tree much more frequently
                "cluster_manager": None,
                # ^ Can be set to, e.g., "slurm", to run a slurm
                # cluster. Just launch one script from the head node.
                "precision": 64,
                # ^ Higher precision calculations.
                "warm_start": True,
                # ^ Start from where left off.
                "turbo": True,
                # ^ Faster evaluation (experimental)
                "julia_project": None,
                # ^ Can set to the path of a folder containing the
                # "SymbolicRegression.jl" repo, for custom modifications.
                "update": False,
                # ^ Don't update Julia packages
                "extra_sympy_mappings": {"cos2": lambda x: sympy.cos(x) ** 2},
                # extra_torch_mappings={sympy.cos: torch.cos},
                # ^ Not needed as cos already defined, but this
                # is how you define custom torch operators.
                # extra_jax_mappings={sympy.cos: "jnp.cos"},
                # ^ For JAX, one passes a string.
            }
        self._method = PySRRegressor(**params)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train method
        self._method.fit(train_x, train_y)

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()
        logging.info(f"PySR MSE is: {mse}")
        logging.info(self._method.sympy())
        result = {
            "method": "PySR",
            "mse": mse,
            "equation": str(self._method.sympy())
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
    method = PysrProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate PySR procedure with data from the path {data_path}.")
        result = {
            "method": f"PySR procedure failed with data from {data_path}",
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

