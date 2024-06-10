import os
import sys
import logging

# Import local methods
from helper_functions import load_dataset
sys.path.append(os.path.join(os.path.dirname(__file__), '../../bench/utils'))
from run_commands import run_commands


class TestMethodProcedure:
    """
    This is a superclass for testing procedures in methods.
    This should never be used directly.
    """

    def test_non_test_variable(self):
        self.assertEqual(isinstance(self.non_test._method, self.regressor), True)

    def test_class_variables(self):
        self.assertEqual(isinstance(self.method._method, self.regressor), True)

    def test_procedure(self):
        dataset = load_dataset()
        result = self.method.procedure(*dataset)
        self.assertIsNotNone(result)
        self.assertEqual(isinstance(result, dict), True)

    def test_main_valid_path(self):
        data_path = "../../../tests/utils/test_dataset.csv"
        result = run_commands([f"python procedure.py --data_path {data_path} --test True"])
        # Clean up
        if os.path.exists("result.json"):
            os.remove("result.json")
        self.assertEqual(result, None)

    def test_main_false_path(self):
        with self.assertRaises(RuntimeError):
            logging.disable(logging.CRITICAL)
            run_commands([f"python procedure.py --data_path wrong.csv"])
            logging.disable(logging.NOTSET)

    def test_main_yields_result_file(self):
        data_path = "../../../tests/utils/test_dataset.csv"
        run_commands([f"python procedure.py --data_path {data_path} --test True"])
        result_file_exists = os.path.exists("result.json")
        # Clean up
        if result_file_exists:
            os.remove("result.json")
        self.assertEqual(result_file_exists, True)