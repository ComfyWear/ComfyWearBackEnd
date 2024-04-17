"""The module containing the classifier for inference the comfort level."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class ComfortClassifier:
    """A comfort level classifier for inference the comfort level."""

    def __init__(self):
        """
        Initialize the comfort level classifier.

        The classifier is a random forest classifier that is trained on a dataset containing
        comfort level labels, clothing item labels, local temperature, and local humidity.
        """
        self.classifier: RandomForestClassifier = RandomForestClassifier()
        self.ds: pd.DataFrame = pd.read_csv("models/data.csv")
        self.columns: pd.Index = self.ds.columns[:-1]
        self.train_classifier()

    def train_classifier(self) -> None:
        """
        Train the comfort level classifier using the loaded dataset.

        The classifier is trained on the dataset containing comfort
        level labels, clothing item labels, local temperature,
        and local humidity.
        """
        X_train: pd.DataFrame = self.ds.drop("comfort_level", axis=1)
        y_train: pd.Series = self.ds["comfort_level"]
        self.classifier.fit(X_train, y_train)

    def predict_comfort_level(self, labels: list[tuple], local_temp: float,
                              local_humid: float) -> list:
        """
        Predict the comfort level.

        :param labels: A list of tuples containing the upper and lower labels.
        :type labels: list[tuple]
        :param local_temp: The local temperature.
        :type local_temp: float
        :param local_humid: The local humidity.
        :type local_humid: float
        :return: The predicted comfort levels.
        :rtype: list
        """
        input_data: list = self._prepare_input_data(labels, local_temp,
                                                    local_humid)
        input_df: pd.DataFrame = pd.DataFrame(input_data, columns=self.columns)
        comfort_levels: np.ndarray = self.classifier.predict(input_df)
        return comfort_levels.tolist()

    def _prepare_input_data(self, labels: list[tuple], local_temp: float,
                            local_humid: float) -> list:
        """
        Prepare the input data for comfort level prediction.

        :param labels: A list of tuples containing the upper and lower labels.
        :type labels: list[tuple]
        :param local_temp: The local temperature.
        :type local_temp: float
        :param local_humid: The local humidity.
        :type local_humid: float
        :return: The prepared input data.
        :rtype: list
        """
        input_data: list = []
        for upper_label, lower_label in labels:
            row_data: list = [0] * len(self.columns)
            if upper_label:
                row_data[self.columns.get_loc(upper_label)] = 1
            if lower_label:
                row_data[self.columns.get_loc(lower_label)] = 1
            row_data[-2] = local_temp
            row_data[-1] = local_humid
            input_data.append(row_data)
        return input_data
