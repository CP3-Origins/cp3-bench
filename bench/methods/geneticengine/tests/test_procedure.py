import os
import sys
from unittest import TestCase
from geneticengine.off_the_shelf.regressors import GeneticProgrammingRegressor

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
from bench.methods.geneticengine.procedure import GeneticengineProcedure

# Import local methods
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../tests/utils'))
from test_method_procedure import TestMethodProcedure


class TestGeneticengineProcedure(TestCase, TestMethodProcedure):

    def setUp(self) -> None:
        self.method = GeneticengineProcedure(test=True)
        self.non_test = GeneticengineProcedure()
        self.regressor = GeneticProgrammingRegressor