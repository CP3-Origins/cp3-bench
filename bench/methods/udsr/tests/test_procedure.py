import os
import sys
from unittest import TestCase
from dso import DeepSymbolicRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.udsr.procedure import UdsrProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestUdsrProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = UdsrProcedure(test=True)
        self.non_test = UdsrProcedure()
        self.regressor = DeepSymbolicRegressor
