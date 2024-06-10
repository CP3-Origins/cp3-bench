import os
import time
import subprocess
import logging
import pandas as pd


# Path of the parent folder
PATH = os.path.dirname(os.path.abspath(__file__))[:-6]


def run_benchmark(method: str, data_path: str, file_name: str) -> dict:
    """
    Run the benchmark of a given method.

    The function takes the following arguments:
        method (string): Method to evaluate
        data_path (string): Relative path to a csv file containing the dataset
        file_name (string): Name of the dataset csv file
    """
    try:
        logging.info(f"Processing {method} with input {file_name}")
        os.chdir(f"{PATH}/methods/{method}/")

        command = [f"unset PYENV_VERSION && python procedure.py --data_path {data_path}"]

        # Run benchmark method
        start_time = time.time()
        output = subprocess.run(command, capture_output=True, shell=True)
        elapsed_time = time.time() - start_time

        # Check that the run was successful
        error_result = output.stderr.decode('utf-8')
        if "[Errno 2] No such file or directory" in error_result:
            raise RuntimeError(error_result)
        if "Error: Invalid value for '--data_path'" in error_result:
            raise RuntimeError(error_result)

        run_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        logging.info(f"Completed evaluation of {method}")
        return {"method": method, "run_time": run_time}
    except RuntimeError as e:
        logging.error(f"Failed to run {method}")
        logging.error(e)
        return {"method": method, "run_time": None}
    finally:
        os.chdir(PATH)
