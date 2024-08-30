import click
import json
import os
import sys
import logging
import numpy as np
from pyoperon.sklearn import SymbolicRegressor

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class OperonProcedure(MethodEvaluator):
    """
    Operon Procedure for benchmark methods.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)

        if test:
            params = {
                "allowed_symbols": "add,sub,mul,div,constant,variable",
                "brood_size": 5,
                "comparison_factor": 0,
                "crossover_internal_probability": 0.9,
                "crossover_probability": 1.0,
                "epsilon": 1e-05,
                "female_selector": "tournament",
                "generations": 1000,
                "initialization_max_depth": 5,
                "initialization_max_length": 10,
                "initialization_method": "btc",
                "irregularity_bias": 0.0,
                "optimizer_iterations": 1,
                "optimizer": 'lm',
                "male_selector": "tournament",
                "max_depth": 3,
                "max_evaluations": 100,
                "max_length": 10,
                "max_selection_pressure": 100,
                "model_selection_criterion": "minimum_description_length",
                "mutation_probability": 0.25,
                "n_threads": 32,
                "objectives": [ 'r2', 'length' ],
                "offspring_generator": "basic",
                "pool_size": 10,
                "population_size": 10,
                "random_state": None,
                "reinserter": "keep-best",
                "time_limit": 60,
                "tournament_size": 1
            }
        else:
            params = {
                "allowed_symbols": "add,sub,mul,div,sin,cos,exp,logabs,sqrtabs,constant,variable",
                "brood_size": 10,
                "comparison_factor": 0,
                "crossover_internal_probability": 0.9,
                "crossover_probability": 1.0,
                "epsilon": 1e-05,
                "female_selector": "tournament",
                "generations": 1000,
                "initialization_max_depth": 5,
                "initialization_max_length": 10,
                "initialization_method": "btc",
                "irregularity_bias": 0.0,
                "optimizer_iterations": 5,
                "optimizer": 'lm',
                "male_selector": "tournament",
                "max_depth": 10,
                "max_evaluations": 1000000,
                "max_length": 50,
                "max_selection_pressure": 100,
                "model_selection_criterion": "minimum_description_length",
                "mutation_probability": 0.25,
                "n_threads": 32,
                "objectives": [ 'r2', 'length' ],
                "offspring_generator": "basic",
                "pool_size": 1000,
                "population_size": 1000,
                "random_state": None,
                "reinserter": "keep-best",
                "time_limit": 3600,
                "tournament_size": 3
            }

        self._method = SymbolicRegressor(**params)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x, train_y)

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()
        model_expression = self._method.get_model_string(self._method.model_, 5)
        logging.info(f"Operon MSE is: {mse}")
        logging.info(model_expression)
        result = {
            "method": "Operon",
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
    method = OperonProcedure(verbose, test)
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
