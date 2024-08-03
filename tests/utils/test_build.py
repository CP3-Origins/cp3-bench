import os
from bench.utils.read_status import read_status

PATH = os.path.dirname(os.path.abspath(__file__))[:len("tests/utils")]


def test_build(status_list: list) -> None:
    for method in status_list:
        for status in method:
            if status == "[x]":
                continue
            else:
                raise ValueError(f"Method {method} not implemented")


if __name__ == "__main__":
    status_file_path = f"{PATH}/STATUS.md"
    PATH = os.path.dirname(os.path.abspath(__file__))
    test_build(status_file_path)
