import os
import sys
from unittest import TestCase
from pyoperon.sklearn import SymbolicRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.operon.procedure import OperonProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestTemplateProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = OperonProcedure(test=True)
        self.non_test = OperonProcedure()
        self.regressor = SymbolicRegressor
