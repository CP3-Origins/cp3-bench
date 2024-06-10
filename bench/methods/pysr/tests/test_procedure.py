import os
import sys
from unittest import TestCase
from pysr import PySRRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.pysr.procedure import PysrProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestPysrProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = PysrProcedure(test=True)
        self.non_test = PysrProcedure()
        self.regressor = PySRRegressor
