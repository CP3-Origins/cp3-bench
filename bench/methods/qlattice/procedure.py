import click
import json
import re
import os
import sys
import logging
import feyn
from sympy import expand
import pandas as pd
import numpy as np

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class QlatticeProcedure(MethodEvaluator):
    """
    Qlattice Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)
        if test:
            self.epochs = 1
            self.complexity = 2
        else:
            self.epochs = 8000
            self.complexity = 8

        # Connecting
        self._method = feyn.QLattice()

    @staticmethod
    def format_output(model, threshold=1e-10, significant=5, keep_all=False):
        """
        Format the equation. If keep_all is False then we drop
        terms with a coefficient less than threshold and we only keep
        significant decimals up to the specified value.

        The function takes the following arguments:
        model (sympy expression):   The expression format
        threshold (float):   The threshold value to consider for dropping terms
        significant (int):  The number of significant decimals to keep in coefficients
        keep_all (boolean): If True then we keep everything, else we drop significant digits and coefficients
        """
        if keep_all:
            return str(model)
        model_string = str(expand(model))
        equation_terms = model_string.split(" ")
        equation = ""

        for term in equation_terms:
            # Add chain terms with plus or minus
            if term == "+" or term == "-":
                equation += term
                continue

            # Check small coefficient
            skip = False
            coefficient = term.split("*")[0]
            small_number = re.findall(r'e-\d*', coefficient)
            for number in small_number:
                if float(f"1{number}") < threshold:
                   skip = True

            # Ignore terms with small coefficients
            if skip:
                continue

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
        # Remap data
        train = train_x
        train['target'] = train_y
        test = test_x
        test['target'] = test_y

        # Sample and train models
        models = self._method.auto_run(
            data=train,
            output_name='target',
            kind='regression',
            n_epochs=self.epochs,
            criterion='bic',
            max_complexity=self.complexity
        )

        # Select best model
        best = models[0]

        sympy_model = best.sympify(symbolic_cat=False, symbolic_lr=True)
        model_expression = self.format_output(sympy_model)
        yhat = best.predict(test)
        mse = np.square(yhat - test_y).mean()
        logging.info(f"QLattice MSE is: {mse}")
        logging.info(model_expression)
        result = {
            "method": "QLattice",
            "mse": mse,
            "equation": model_expression,
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
    method = QlatticeProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate Qlattice procedure with data from the path {data_path}.")
        result = {
            "method": f"Qlattice procedure failed with data from {data_path}",
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
