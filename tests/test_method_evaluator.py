import os
import sys
import pathlib
import logging
import subprocess
import pandas as pd
from unittest import TestCase

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from bench.utils.method_evaluator import MethodEvaluator

PATH = pathlib.Path(__file__).parent.resolve()


class TestMethodEvaluator(TestCase):

    def setUp(self) -> None:
        self.dataset = f"{PATH}/utils/test_dataset.csv"
        self.initiated_evaluator = MethodEvaluator()
        self.expected_result = {
            "method": "Procedure not defined",
            "mse": 0,
            "equation": "Place holder"
        }

    def test_init_logging_level_1(self):
        log_level = MethodEvaluator(1).log_level
        self.assertEqual(logging.DEBUG, log_level)

    def test_init_logging_level_2(self):
        log_level = MethodEvaluator(2).log_level
        self.assertEqual(logging.INFO, log_level)

    def test_init_logging_level_3(self):
        log_level = MethodEvaluator(3).log_level
        self.assertEqual(logging.WARNING, log_level)

    def test_init_logging_level_4(self):
        log_level = MethodEvaluator(4).log_level
        self.assertEqual(logging.ERROR, log_level)

    def test_init_logging_level_5(self):
        log_level = MethodEvaluator(5).log_level
        self.assertEqual(logging.CRITICAL, log_level)

    def test_load(self):
        train_x, test_x, train_y, test_y = self.initiated_evaluator._MethodEvaluator__load(self.dataset)

        # Test training data
        self.assertEqual(train_y.name, "target")
        self.assertEqual(isinstance(train_y, pd.Series), True)
        self.assertEqual(len(train_x.columns) >= 1, True)

        # Test testing data
        self.assertEqual(test_y.name, "target")
        self.assertEqual(isinstance(test_y, pd.Series), True)
        self.assertEqual(len(test_x.columns) >= 1, True)

        # Test training data
        x_dict_train = train_x.to_dict()
        y_dict_train = train_y.to_dict()

        self.assertEqual(x_dict_train["val"][0], -0.11)
        self.assertEqual(x_dict_train["z"][0], 0.122)
        self.assertEqual(y_dict_train[0], 0.181495558)

        # Test testing data
        x_dict_test = test_x.to_dict()
        y_dict_test = test_y.to_dict()

        self.assertEqual(x_dict_test["val"][1], -0.99)
        self.assertEqual(x_dict_test["z"][1], 0.118)
        self.assertEqual(y_dict_test[1], 0.526882225)

    def test_procedure_with_input(self):
        result = self.initiated_evaluator.procedure(1, 2, 3, 4)
        self.assertEqual(result, self.expected_result)

    def test_procedure_no_input(self):
        with self.assertRaises(Exception) as context:
            self.initiated_evaluator.procedure()
            self.assertTrue('Data does not exist.' in context.exception)

    def test_evaluate_valid_path(self):
        result = self.initiated_evaluator.evaluate(self.dataset)
        self.assertEqual(result, self.expected_result)

    def test_evaluate_invalid_path(self):
        logging.disable(logging.CRITICAL)
        result = self.initiated_evaluator.evaluate("/wrong.json")
        logging.disable(logging.NOTSET)
        self.assertEqual(result, 1)
