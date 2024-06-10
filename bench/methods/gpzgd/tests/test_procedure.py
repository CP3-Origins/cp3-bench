import os
import sys
from unittest import TestCase

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.gpzgd.procedure import GpzgdProcedure
from bench.methods.gpzgd.gpzgd.regressor import GPZGD

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestGpzgdProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = GpzgdProcedure(test=True)
        self.non_test = GpzgdProcedure()
        self.regressor = GPZGD
