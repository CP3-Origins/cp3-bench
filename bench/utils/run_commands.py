import os
import logging


def run_commands(commands: list) -> None:
    """
    Runs bash commands for installation and setup.
    The unset command in front is to ensure that the local version is used.
    If a failure occurs, it will cause a RuntimeError.

    The function takes the following arguments:
        commands (list): A list of commands to perform.
    """
    for command in commands:
        output = os.system(f"unset PYENV_VERSION && {command}")
        if output == 0:
            continue
        else:
            logging.error(f"The following command failed to execute: {command}")
            logging.error(f"Exit code: {output}")
            raise RuntimeError
