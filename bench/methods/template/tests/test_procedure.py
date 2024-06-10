import os
import sys
from unittest import TestCase
from sklearn.linear_model import LinearRegression

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.template.procedure import TemplateProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestTemplateProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = TemplateProcedure(test=True)
        self.non_test = TemplateProcedure()
        self.regressor = LinearRegression
