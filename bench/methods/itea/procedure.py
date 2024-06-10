import click
import json
import os
import sys
import re
import logging
import numpy as np
import pyITEA as itea

# Method to Procedure superclass
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = os.path.dirname(os.path.abspath(__file__))


class IteaProcedure(MethodEvaluator):
    """
    ITEA Procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
        test (boolean):  Whether to run the Class in test mode or not.
    """
    def __init__(self, verbose=2, test=False):
        super().__init__(verbose)

        if test:
            params = {
                "npop": 100,
                "ngens": 100,
                "exponents": (-3, 3),
                "termlimit": (1, 5),
                "nonzeroexps": 10
            }

        else:
            params = {
                "npop": 1000,
                "ngens": 7000,
                "exponents": (-5, 5),
                "termlimit": (1, 5),
                "nonzeroexps": 20,
                "transfunctions": "[Id, Sin, Cos, SqrtAbs, Log, Exp]"
            }

        self._method = itea.ITEARegressor(**params)

    def format_output(self, threshold=1e-10, significant=5, keep_all=False):
        """
        Format the equation. If keep_all is False then we drop
        terms with a coefficient less than threshold and we only keep
        significant decimals up to the specified value.

        The function takes the following arguments:
        threshold (float):   The threshold value to consider for dropping terms
        significant (int):  The number of significant decimals to keep in coefficients
        keep_all (boolean): If True then we keep everything, else we drop significant digits and coefficients
        """
        if keep_all:
            return self._method.sympy
        equation_terms = self._method.sympy.split("+")
        equation = ""

        for term in equation_terms:
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
            equation += term + "+"

        return equation[:-1]

    def procedure(self, train_x, test_x, train_y, test_y) -> dict:
        # Train model
        self._method.fit(train_x, train_y)

        yhat = self._method.predict(test_x)
        mse = np.square(yhat - test_y).mean()
        equation = self.format_output()
        logging.info(f"ITEA MSE is: {mse}")
        logging.info(equation)
        result = {
            "method": "ITEA",
            "mse": mse,
            "equation": equation
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
    method = IteaProcedure(verbose, test)
    result = method.evaluate(data_path)
    if result == 1:
        logging.error(f"Failed to evaluate ITEA procedure with data from the path {data_path}.")
        result = {
            "method": f"ITEA procedure failed with data from {data_path}",
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
