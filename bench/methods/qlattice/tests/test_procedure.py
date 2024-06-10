import os
import sys
import feyn
from unittest import TestCase

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.qlattice.procedure import QlatticeProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestQlatticeProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = QlatticeProcedure(test=True)
        self.non_test = QlatticeProcedure()
        self.regressor = feyn.QLattice
