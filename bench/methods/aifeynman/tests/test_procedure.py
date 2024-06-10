import os
import sys
from unittest import TestCase
from aifeynman import AIFeynmanRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.aifeynman.procedure import AifeynmanProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestAifeynmanProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = AifeynmanProcedure(test=True)
        self.non_test = AifeynmanProcedure()
        self.regressor = AIFeynmanRegressor
