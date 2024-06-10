import os
import sys
import pyITEA as itea
from unittest import TestCase

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.itea.procedure import IteaProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestIteaProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = IteaProcedure(test=True)
        self.non_test = IteaProcedure()
        self.regressor = itea.ITEARegressor
