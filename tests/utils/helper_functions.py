import pathlib
import pandas as pd
from sklearn.model_selection import train_test_split

PATH = pathlib.Path(__file__).parent.resolve()


def load_dataset() -> tuple:
    df = pd.read_csv(f"{PATH}/test_dataset.csv")
    x = df.loc[:, df.columns != "target"]
    y = df.loc[:, "target"]
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42)
    return train_x, test_x, train_y, test_y
