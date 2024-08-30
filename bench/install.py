import logging
import glob
import os
import json
import click
from subprocess import run

#Local imports
from utils.run_commands import run_commands
from utils.read_status import read_status
from utils.methods_handler import methods_handler

PATH = os.path.dirname(os.path.abspath(__file__))
METHODS = [folder[:-1] for folder in glob.glob("**/", root_dir=f"{PATH}/methods") if folder[:-1] != "__pycache__"]

logging.basicConfig(level=logging.INFO)


def install(methods: str, reinstall: bool) -> None:
    """
    Install script for benchmark.

    This script will install the selected methods and report the
    status of the methods in a STATUS.md file. If something goes wrong,
    you may use the reinstall flag to reinstall a given method.

    The function takes the following arguments:
        methods (string): The methods to install
        reinstall (bool): Whether to reinstall the selected methods
    """
    # Set and verify selected methods
    selected_methods = methods_handler(methods)

    # Read status file
    status_file_path = f"{PATH}/STATUS.md"
    status_list = []
    if os.path.exists(status_file_path):
        status_list = read_status(status_list, status_file_path)
    else:
        logging.debug(f"No {status_file_path}. It will be created.")

    for method in selected_methods:
        if method == "template":
            logging.warning("The template method is disabled and will not be installed!")
            continue

        # Load status from STATUS.md if status exists otherwise flags are False
        status_dir = {
            "config": False,
            "env": False,
            "install": False,
            "tests": False,
        }

        for status in status_list:
            if status["method"] == method:
                for key, value in status.items():
                    if key == "method":
                        continue
                    status_dir[key] = True if value == "[x]" else False

        # Load config for method
        try:
            with open(f"{PATH}/methods/{method}/config.json", 'r') as config_file:
                config = json.load(config_file)

            # Ensure the config is correct
            config_keys = [
                "name",
                "key",
                "python_version",
                "install_commands"
            ]
            assert list(config.keys()) == config_keys

            # Validate Python version
            if config['python_version'].count(".") == 0:
                raise AssertionError(
                    f"Python version {config['python_version']} is not valid."
                    f"Please specify a version like 2.5 or 3.9 or 3.8.10."
                )

            status_dir["config"] = True
            logging.debug("Config loaded successfully")
        except FileNotFoundError as e:
            logging.error(f"Configuration file not found for {method}.")
            logging.error(f"Error message: {e}")

        # Ensure that method to uninstall is installed, or at least has an environment created.
        if reinstall and status_dir["env"] is False:
            raise AssertionError("Cannot reinstall method that isn't installed")

        # Reinstall
        if reinstall:
            try:
                logging.debug(f"Trying to uninstall: {config['name']}")
                # Change to method dir
                os.chdir(f"{PATH}/methods/{method}")

                # Note we remove everything in the deps dir, so other directories persist
                commands= [
                    f"pyenv virtualenv-delete {config['key']}",
                    f"rm -rf deps"
                ]
                # Remove python version
                run_commands(commands)

                # Update status flags
                status_dir = {
                    "config": True,
                    "env": False,
                    "install": False,
                    "tests": False,
                }

                logging.info(f"Successfully uninstalled: {config['name']}")
            except RuntimeError:
                logging.error(f"Could not uninstall: {config['name']}.")
            finally:
                # Return to script dir
                os.chdir(PATH)

        # Setup env and python requirements
        if status_dir["env"] is False:
            try:
                # Change to method dir
                os.chdir(f"{PATH}/methods/{method}")

                # Storing installation and setup commands
                commands = []

                # Determine installed pyenv versions and environments
                python_exists = False
                environment_exists = False

                pyenv_versions = run(['pyenv', 'versions'], capture_output=True).stdout.decode("utf-8").split("\n")
                for output in pyenv_versions:
                    trimmed_value = output.strip()

                    # Check if Python version is already installed
                    split_list = trimmed_value.split("/")
                    for value in split_list:
                        if value.count('.') == 2 and config['python_version'] in value:
                            python_exists = True

                    for value in split_list:
                        if " --> " in value:
                            if f"{config['key']}" == value.split(" --> ")[0]:
                                environment_exists = True

                # If the environment already exists do not create it
                if environment_exists:
                    logging.info(f"Virtual environment named {config['key']} already exists.")
                else:
                    commands.append(f"pyenv virtualenv {config['python_version']} {config['key']}")
                    logging.info(f"A virtual environment will be created for: {config['name']}")

                # Append remaining commands
                commands.extend([
                    f"pyenv local {config['python_version']}",
                    f"pyenv local {config['key']}",
                    "pip install -r requirements.txt"
                ])

                # Perform install and setup commands
                run_commands(commands)

                # Ensure the version is correctly set
                local_python = run(
                    ['unset PYENV_VERSION && python -V'], shell=True,
                    capture_output=True
                ).stdout.decode("utf-8")
                if config['python_version'] not in local_python:
                    logging.error(f"Failed to initialize Python version {config['python_version']}.")
                    logging.error(f"The local Python version is {local_python}.")
                    raise RuntimeError

                # Everything was successful
                logging.info(f"Setup of pyenv for {config['name']} complete.")
                status_dir["env"] = True
            except RuntimeError:
                logging.error(f"Could not setup python environment for method: {config['name']}.")
            finally:
                # Return to script dir
                os.chdir(PATH)

        # Install dependencies
        if status_dir["install"] is False and status_dir["env"]:
            try:
                # Change to method dir
                os.chdir(f"{PATH}/methods/{method}")

                # Run install commands
                run_commands(config["install_commands"])

                logging.info(f"Installation completed for method: {method}.")
                status_dir["install"] = True
            except RuntimeError:
                logging.error(f"Could not install: {method}.")
            finally:
                # Return to script dir
                os.chdir(PATH)

        # Run tests
        if status_dir["tests"] is False and status_dir["install"]:
            try:
                os.chdir(f"{PATH}/methods/{method}")
                run_commands(["coverage run -m unittest discover"])
                logging.info(f"Coverage run complete for method: {config['name']}.")
                status_dir["tests"] = True
            except RuntimeError:
                logging.error(f"Test failed for method: {config['name']}.")
            finally:
                # Return to script dir
                os.chdir(PATH)

        # Evaluate the installation
        if all(list(status_dir.values())):
            logging.info(f"{config['name']} is installed successfully!")
        else:
            logging.warning(f"{config['name']} is not installed!")

        # Save result to status list and remove the previous entry if it exists
        status_list = [status for status in status_list if status["method"] != method]
        result_dir = {
            "method": method,
            "config": "[x]" if status_dir["config"] else "[-]",
            "env": "[x]" if status_dir["env"] else "[-]",
            "install": "[x]" if status_dir["install"] else "[-]",
            "tests": "[x]" if status_dir["tests"] else "[-]"
        }
        status_list.append(result_dir)

    # Sort our status list
    sorted_status_list = sorted(status_list, key=lambda d: d['method'])

    with open(status_file_path, "w") as status_file:
        status_string = ("| Method       | Config | Environment | Installation | Tests |\n"
                         "|--------------|:------:|:-----------:|:------------:|:-----:|\n")
        for status in sorted_status_list:
            tmp_string = (f"|{status['method']:<14}"
                          f"|{status['config']:^8}"
                          f"|{status['env']:^13}"
                          f"|{status['install']:^14}"
                          f"|{status['tests']:^7}"
                          "|\n")
            status_string += tmp_string
        # Write the new status file
        status_file.write(status_string)

    logging.info(f"STATUS.md updated!")


@click.command()
@click.option(
    "--methods",
    default="all",
    help=f"Select methods to install as a comma seperated string e.g dsr,dso. "
         f"Default is to install all. Available methods are: {METHODS}"
)
@click.option(
    "--reinstall",
    default=False,
    help=f"Flag to trigger a reinstall of the selected method or methods."
)
def main(methods: str, reinstall: bool) -> None:
    """
    CLI entry point for installing the benchmark package.
    methods

    The function takes the following arguments:
        methods (string): The methods to install
        reinstall (bool): Whether to reinstall the selected methods
    """
    install(methods, reinstall)


if __name__ == "__main__":
    """
    This function runs all the installation steps for each benchmark method including:
        1. Load the configuration file
        2. Create the Python environment
        3. Install the Python dependencies
        4. Install the benchmark method
        5. Test the installation and method
    
    The function takes the following arguments:
        methods (str):      A comma separated list of methods to use in the form of a string. E.g. 'dsr,pso,gpzgd'
                            This method as a default special key called 'all' which installs all packages.
        reinstall (bool):   If True the selected methods will be reinstalled. Default is False.
    """
    main()