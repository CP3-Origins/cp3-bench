import click
import json
import os
import sys
import logging
import numpy as np
from sympy import sympify, expand
from geneticengine.off_the_shelf.regressors import GeneticProgrammingRegressor

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class GeneticengineProcedure(MethodEvaluator):
    """
    Genetic Engine Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)
        if test:
            params = {
                "population_size": 10,
                "n_elites": 2,
                "n_novelties": 5,
                "max_depth": 10,
                "favor_less_deep_trees": True,
                "seed": 5,
                "hill_climbing": True,
                "probability_mutation": 0.01,
                "probability_crossover": 0.8,
                "timer_stop_criteria": True,
                "timer_limit": 5,
                "metric": 'mse'
            }
        else:
            params = {
                "population_size": 500,
                "n_elites": 20,
                "n_novelties": 40,
                "number_of_generations": 2000,
                "max_depth": 14,
                "favor_less_deep_trees": True,
                "seed": 123,
                "hill_climbing": True,
                "probability_mutation": 0.2,
                "probability_crossover": 0.9,
                "timer_stop_criteria": True,
                "timer_limit": 14400, # 4 Hours
                "metric": 'mse'
            }

        self._method = GeneticProgrammingRegressor(**params)

    def format_output(self):
        """
        Simplify and format the equation.
        """
        equation_raw = str(self._method.evolved_phenotype)
        equation = equation_raw.replace("np.", "")
        equation_simple = expand(sympify(equation))
        return str(equation_simple)

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train method
        self._method.fit(train_x, train_y)

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()

        model_expression = self.format_output()
        logging.info(f"GeneticEngine MSE is: {mse}")
        logging.info(model_expression)
        result = {
            "method": "GeneticEngine",
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
    method = GeneticengineProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate Genetic Engine procedure with data from the path {data_path}.")
        result = {
            "method": f"Genetic Engine procedure failed with data from {data_path}",
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

