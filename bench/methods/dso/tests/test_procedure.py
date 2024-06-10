import os
import sys
import pandas as pd
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from dso import DeepSymbolicRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.dso.procedure import DsoProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from helper_functions import load_dataset



class TestDsoProcedure(TestCase):

    def setUp(self) -> None:
        self.method = DsoProcedure(test=True)
        self.dataset = load_dataset()

    def test_non_test_variable(self):
        non_test = DsoProcedure()
        self.assertEqual(isinstance(non_test._method, DeepSymbolicRegressor), True)

    def test_class_variables(self):
        self.assertEqual(isinstance(self.method._method, DeepSymbolicRegressor), True)

    def test_procedure(self):
        result = self.method.procedure(*self.dataset)
        self.assertIsNotNone(result)
        self.assertEqual(isinstance(result, dict), True)
