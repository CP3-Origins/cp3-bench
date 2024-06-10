import os
import sys
import pathlib
from unittest import TestCase

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from bench.utils.read_status import read_status

PATH = pathlib.Path(__file__).parent.resolve()


class TestReadStatus(TestCase):

    def setUp(self) -> None:
        self.status = f"{PATH}/utils/test_STATUS.md"
        self.result = {'method': 'template', 'config': '[x]', 'env': '[x]', 'install': '[x]', 'tests': '[x]'}

    def test_read_status_return_list(self):
        input_list = []
        output_list = read_status(input_list, self.status)
        self.assertEqual(isinstance(output_list, list), True)
        self.assertEqual(output_list[0], self.result)