import os
import sys
from unittest import TestCase
from dsr import DeepSymbolicRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.dsr.procedure import DsrProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestDsrProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = DsrProcedure(test=True)
        self.non_test = DsrProcedure()
        self.regressor = DeepSymbolicRegressor
