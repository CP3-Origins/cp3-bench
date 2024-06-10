import os
import sys
import logging
from unittest import TestCase

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from bench.utils.run_commands import run_commands


class TestRunCommands(TestCase):

    def test_correct_command(self):
        result = run_commands(["echo Hello World!"])
        self.assertEqual(result, None)

    def test_incorrect_command(self):
        with self.assertRaises(RuntimeError):
            logging.disable(logging.CRITICAL)
            run_commands(["This will not work"])
            logging.disable(logging.NOTSET)
