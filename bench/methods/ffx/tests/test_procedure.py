import os
import sys
from unittest import TestCase
from ffx import FFXRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.ffx.procedure import FfxProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestFfxProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = FfxProcedure()
        self.non_test = FfxProcedure()
        self.regressor = FFXRegressor
