import os
import sys
import logging
from unittest import TestCase

# Local import
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from bench.utils.read_status import read_status

PATH = os.path.dirname(os.path.abspath(__file__))[:-len("tests/utils")]


def test_build(status_list: str) -> int:
    for method in status_list:
        if method["tests"] == "[x]":
            continue
        else:
            logging.error(f"Method {method} has not been implemented")
            return 1
    return 0
            
class TestBuild(TestCase):

    def test_build_all_success(self):
        status_file_path = f"{PATH}/STATUS.md"
        status_list = read_status(status_file_path)
        output = test_build(status_list)
        self.assertEqual(output, 0)
        logging.info("All tests passed")
