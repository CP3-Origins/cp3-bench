import os
import sys
import pathlib
import logging
import glob
from unittest import TestCase

# Method to test
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from bench.utils.methods_handler import methods_handler

logging.basicConfig(level=logging.CRITICAL)
PATH = pathlib.Path(__file__).parent.resolve()
METHODS = [folder[:-1] for folder in glob.glob("**/", root_dir=f"{PATH}/../bench/methods")
           if folder[:-1] != "__pycache__"]


class TestMethodsHandler(TestCase):

    def test_all_returns_all_methods(self):
        expected_result = METHODS
        result = methods_handler("all")
        self.assertEqual(result, expected_result)

    def test_comma_list(self):
        expected_result = ["template", "dso", "dsr"]
        result = methods_handler("template,dso,dsr")
        self.assertEqual(result, expected_result)

    def test_single_selection(self):
        expected_result = ["template"]
        result = methods_handler("template")
        self.assertEqual(result, expected_result)

    def test_false_selection(self):
        with self.assertRaises(NameError):
            logging.disable(logging.CRITICAL)
            methods_handler("this,does,not,exist")
            logging.disable(logging.NOTSET)

    def test_false_type(self):
        with self.assertRaises(TypeError):
            logging.disable(logging.CRITICAL)
            methods_handler(123)
            logging.disable(logging.NOTSET)
