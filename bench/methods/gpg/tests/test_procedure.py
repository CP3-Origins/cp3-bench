import os
import sys
from unittest import TestCase
from pygpg.sk import GPGRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.gpg.procedure import GpgProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestTemplateProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = GpgProcedure(test=True)
        self.non_test = GpgProcedure()
        self.regressor = GPGRegressor
