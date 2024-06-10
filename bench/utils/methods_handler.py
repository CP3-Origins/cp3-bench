import os
import logging
import glob

PATH = os.path.dirname(os.path.abspath(__file__))
METHODS = [folder[:-1] for folder in glob.glob("**/", root_dir=f"{PATH}/../methods") if folder[:-1] != "__pycache__"]


def methods_handler(methods: str) -> list:
    """
    This function converts the input string of methods into
    a list of methods and verify that they are valid methods.

    The function takes the following arguments:
        methods (string): Methods to select and verify
    """
    # Test correct input type
    if not isinstance(methods, str):
        logging.critical("Method input is not a list")
        raise TypeError(f"Method input is a {type(methods)} and not a list")

    # The all keyword installs all methods
    if methods == "all":
        selected_methods = METHODS
    elif "," in methods:
        selected_methods = methods.split(",")
    else:
        selected_methods = [methods]

    # Test validity of methods
    for method in selected_methods:
        if method not in METHODS:
            logging.critical("Invalid method(s) selected")
            raise NameError(f"Not all of the elements {methods} are found in {METHODS}")

    return selected_methods
