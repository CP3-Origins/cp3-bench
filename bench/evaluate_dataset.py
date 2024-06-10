import os
import sys
import logging
import time
import click
import pandas as pd
from multiprocessing import Pool

# Local imports
sys.path.append(os.path.join(os.path.dirname(__file__), ''))
from utils.read_status import read_status
from utils.run_benchmark import run_benchmark
from utils.methods_handler import methods_handler

# Set log level
logging.basicConfig(level=logging.INFO)

PATH = os.path.dirname(os.path.abspath(__file__))


def evaluate_dataset(data_path: str, methods: str = "all") -> None:
    """
    Evaluate the performance of the installed methods for a given dataset.

    The function takes the following arguments:
        data_path (string): The relative path to a csv file containing the dataset
        methods (string): The methods to use to evaluate the dataset
    """
    # Set basic variables
    df = pd.DataFrame(columns=["method", "mse", "equation", "run_time"])

    # Check data_path
    if ".csv" not in data_path:
        raise TypeError("Data path must point to a .csv file.")
    file_name = data_path.split("/")[-1]

    # Set and verify selected methods
    selected_methods = methods_handler(methods)

    # Read status file
    status_file_path = f"{PATH}/STATUS.md"
    status_list = []
    if os.path.exists(status_file_path):
        status_list = read_status(status_list, status_file_path)
    else:
        logging.error(
            f"No {status_file_path}. "
            f"Please install at least one method to run."
            "This can be done by running `python install.py`.")
        raise RuntimeError

    methods_to_process = []
    for status in status_list:
        if status["method"] in selected_methods:
            logging.debug(f"Method {status['method']} exists.")
        else:
            continue

        if status["tests"] == "[x]":
            logging.debug(f"Method {status['method']} is installed.")
            methods_to_process.append(status["method"])
        else:
            logging.warning(f"Method {status['method']} is not installed and will be skipped.")

    if not os.path.exists(f"{PATH}/results"):
        logging.debug("Creating results folder")
        os.makedirs(f"{PATH}/results")

    try:
        # Determine cores
        cores = os.cpu_count() - 1 if os.cpu_count() > 1 else 1

        # Configure arguments
        args = [(method, data_path, file_name) for method in methods_to_process]

        # Multicore processing
        with Pool(cores) as p:
            results = p.starmap(run_benchmark, args)
            
            # Report all tasks done
            logging.info("All methods have been benchmarked")

        # Collect and save results
        for method_result in results:
            method = method_result["method"]
            run_time = method_result["run_time"]

            if run_time is None:
                logging.error(f"Method {method} failed to run")
                continue
            result_file_name = "result.json"
            result_string = f"{PATH}/methods/{method}/{result_file_name}"

            try:
                # Save result
                logging.info(f"Saving output for: {method}")
                with open(result_string, 'r') as result_file:
                    output = pd.read_json(result_file, typ="series")
                    time_series = pd.Series([run_time], index=["run_time"])
                    result = pd.concat([output, time_series])
                    df = pd.concat([df, result.to_frame().T])
                logging.info(f"Successfully ran {method}")
            except FileNotFoundError as e:
                logging.error(f"Result missing for {method}")
                logging.error(e)
            # Clean up and return
            if os.path.exists(result_string):
                os.remove(result_string)
    finally:
        # If the procedure interrupts, save output
        ts = str(time.time()).replace(".", "-")
        df.to_csv(f"{PATH}/results/result-{file_name[:-4]}-{ts}.csv", encoding="utf-8", index=False)
        logging.info(f"Completed evaluating data from: {file_name}.")


@click.command()
@click.option(
    "--data_path",
    help="Absolute path to the data set of .csv format."
)
@click.option(
    "--methods",
    default="all",
    help="Selected methods to benchmark."
)
def main(data_path: str, methods: str = "all") -> None:
    """
    CLI entry point for installing the benchmark package.
    methods

    The function takes the following arguments:
        data_path (string): Path to the dataset
        methods (string): The methods to use to evaluate the dataset
    """
    evaluate_dataset(data_path, methods)


if __name__ == "__main__":
    """
    This function executes the benchmark for a given data path

    The function takes the following arguments:
        data_path (string): Path to the dataset
        methods (string): The methods to use to evaluate the dataset
    """
    main()
