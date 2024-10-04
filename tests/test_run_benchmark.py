import os
import sys
import pathlib
import logging
import subprocess
from unittest import TestCase, mock
from unittest.mock import patch

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from bench.utils.run_benchmark import run_benchmark

logging.basicConfig(level=logging.CRITICAL)
PATH = pathlib.Path(__file__).parent.resolve()


class TestRunBenchmark(TestCase):

    def setUp(self) -> None:
        self.kwargs = {
            "method": "template",
            "data_path": "test.path",
            "file_name": "test.csv"
        }

    def test_invalid_path(self):
        expected_result = {"method": "template", "run_time": None}
        result = run_benchmark(**self.kwargs)
        self.assertEqual(result, expected_result)

    def test_invalid_method(self):
        with self.assertRaises(FileNotFoundError):
            kwargs = {
                "method": "wrong",
                "data_path": "test.path",
                "file_name": "test.csv"
            }
            run_benchmark(**kwargs)

    @patch('subprocess.run')
    def test_shell_command_is_run(self, mock_run):
        mock_run.side_effect = None
        result = run_benchmark(**self.kwargs)
        self.assertEqual(result["method"], "template")
        self.assertIsNotNone(result["run_time"])
        self.assertTrue(mock_run.called)
