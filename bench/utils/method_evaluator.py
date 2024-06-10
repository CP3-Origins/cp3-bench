import click
import logging
import pandas as pd
from sklearn.model_selection import train_test_split


class MethodEvaluator:
    """
    Superclass for the benchmark procedure to set common properties.
    It contains the loading mechanism for the procedure to load a
    dataset such that it can be ingested into test procedure.
    It contains a dummy procedure to be overwritten by the benchmark procedures.
    Then it contains a function with CLI interfacing for the benchmark procedure.

    The function takes the following arguments:
        verbose (int):   The level of verbosity of logging.
    """
    def __init__(self, verbose=2):
        if verbose == 1:
            self.log_level = logging.DEBUG
        elif verbose == 2:
            self.log_level = logging.INFO
        elif verbose == 3:
            self.log_level = logging.WARNING
        elif verbose == 4:
            self.log_level = logging.ERROR
        elif verbose == 5:
            self.log_level = logging.CRITICAL
        else:
            raise ValueError(
                "Invalid verbose value. The value must be an integer between 1 and 5"
                "Valid values are: 1 (DEBUG), 2 (INFO), 3 (WARNING), 4 (ERROR), 5 (CRITICAL)"
            )
        # Set log level
        logging.basicConfig(level=self.log_level)

    @staticmethod
    def __load(data_path):
        """
        This method loads the csv dataset into a pandas dataframe.
        Then it splits the dataset into training and testing sets.
        """
        df = pd.read_csv(data_path)
        x = df.loc[:, df.columns != "target"]
        y = df.loc[:, "target"]
        train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42)
        return train_x, test_x, train_y, test_y

    @staticmethod
    def procedure(train_x, test_x, train_y, test_y) -> dict:
        """
        This procedure must be overwritten by the benchmark procedure using
        this superclass.
        """
        if all([str(train_x), str(test_x), str(train_y), str(test_y)]):
            logging.debug("Data exists")
        else:
            raise ValueError("Data does not exist.")

        result = {
            "method": "Procedure not defined",
            "mse": 0,
            "equation": "Place holder"
        }
        return result

    def evaluate(self, data_path) -> dict:
        try:
            data = self.__load(data_path)
            result = self.procedure(*data)
            return result
        except FileNotFoundError:
            logging.error(f"File with path {data_path} not found.")
            return 1
