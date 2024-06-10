import click
import json
import os
import re
import sys
import logging
import numpy as np

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator
from bench.methods.gpzgd.gpzgd.regressor import GPZGD

PATH = os.path.dirname(os.path.abspath(__file__))


class GpzgdProcedure(MethodEvaluator):
    """
    GPZGD Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)
        if test:
            params = {
                "pop_size": 5,
                "generations": 2,
                "tournament_size": 3,
                "validation_prop": 0.0,
                "crossover_rate": 0.3,
                "sub_mutation_rate": 0.4,
                "point_mutation_rate": 0.3,
                "mutation_sigma": 0.1,
                "min_tree_init": 2,
                "max_tree_init": 4,
                "max_tree_nodes": 20,
                "opset": "ADD,SUB,MUL,SIN,ERC,VAR",
                "learning_rate": 0.01,
                "learning_epochs": 3,
                "timeout": 0,
                "random_state": -1
            }
        else:
            params = {
                "pop_size": 200,
                "generations": 5000,
                "tournament_size": 4,
                "validation_prop": 0.01,
                "crossover_rate": 0.2,
                "sub_mutation_rate": 0.4,
                "point_mutation_rate": 0.3,
                "mutation_sigma": 0.1,
                "min_tree_init": 2,
                "max_tree_init": 5,
                "max_tree_nodes": 8,
                "opset": "ADD,SUB,MUL,SIN,ERC,VAR",
                "learning_rate": 0.001,
                "learning_epochs": 5000,
                "timeout": 14400,
                "random_state": 1
            }

        self._method = GPZGD(**params)

    @staticmethod
    def format_output(model, threshold=1e-10, significant=5, keep_all=False):
        """
        Format the equation. If keep_all is False then we only keep
        significant decimals up to the specified value.

        The function takes the following arguments:
        model (str):   The expression format
        threshold (float):   The threshold value to consider for dropping terms
        significant (int):  The number of significant decimals to keep in coefficients
        keep_all (boolean): If True then we keep everything, else we drop significant digits and coefficients
        """
        if keep_all:
            return str(model)
        model_string = str(model)
        equation_terms = model_string.split(" ")
        equation = ""

        for term in equation_terms:
            # Check for floats with too many digits
            terms_to_round = re.findall(r'[0-9]*\.[0-9]{'
                                        f'{significant}'
                                        r',}', term)
            for float_value in terms_to_round:
                # Check for small numbers -> Put them to zero
                if float(float_value) < threshold:
                    term = term.replace(float_value, str(0))
                # Round to specified decimal
                new_value = round(float(float_value), significant)
                term = term.replace(float_value, str(new_value))
            equation += term

        return equation

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train method
        self._method.fit(train_x, train_y)

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()
        model_expression = self.format_output(self._method.expr_str())
        logging.info(f"gpzgd MSE is: {mse}")
        logging.info(model_expression)
        result = {
            "method": "gpzgd",
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
    method = GpzgdProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate GPZGD procedure with data from the path {data_path}.")
        result = {
            "method": f"GPZGD procedure failed with data from {data_path}",
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

