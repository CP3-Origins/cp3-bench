import os
import logging

PATH = os.path.dirname(os.path.abspath(__file__))[:-len("/utils")]


def read_status(status_list: list, filename: str=f"{PATH}/STATUS.md") -> list:
    """
    Reads the status of the STATUS.md file as default
    and returns a list of dictionaries containing the status of the
    installed methods.

    The function takes the following arguments:
        status_list (list): A list to store results.
        filename (string):  Name of status file.
    """
    logging.debug(f"Reading {filename}")
    with open(filename, "r") as status_file:
        status_lines = status_file.readlines()[2:]
        for line in status_lines:
            line_list = line.split("|")

            # Save list content
            line_content = {
                "method": line_list[1].strip(),
                "config": line_list[2].strip(),
                "env": line_list[3].strip(),
                "install": line_list[4].strip(),
                "tests": line_list[5].strip()
            }
            status_list.append(line_content)
    return status_list
