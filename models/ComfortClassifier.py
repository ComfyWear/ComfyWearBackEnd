"""The module containing the classifier for inference the comfort level."""
import joblib
import numpy as np
import pandas as pd


class ComfortClassifier:
    """A comfort level classifier for inference the comfort level."""

    def __init__(self):
        """
        Initialize the comfort level classifier.

        The classifier is a random forest classifier that is trained on a dataset containing
        comfort level labels, clothing item labels, local temperature, and local humidity.
        """
        self.classifier = joblib.load("models/weights/mlp_model.pkl")
        self.columns = pd.read_csv("models/model_resources/data.csv").columns[:-1]

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
        input_df: pd.DataFrame = pd.DataFrame(input_data)
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
                upper_label = self._map_input(upper_label)
                row_data[self.columns.get_loc(upper_label)] = 1
            if lower_label:
                lower_label = self._map_input(lower_label, False)
                row_data[self.columns.get_loc(lower_label)] = 1
            row_data[-2] = local_temp
            row_data[-1] = local_humid
            input_data.append(row_data)
        return input_data

    def _map_input(self, label: str, is_upper=True) -> str:
        """
        Map the input label to the corresponding label in the dataset.

        :param label: The input label.
        :type label: str
        :param is_upper: A flag indicating whether the label is for the upper or lower body.
        :type is_upper: bool
        :return: The mapped label.
        :rtype: str
        """
        upper_mapping = {
            "long sleeve dress": "long sleeve top",
            "short sleeve dress": "short sleeve top",
            "sling": "long sleeve top",
            "sling dress": "short sleeve top",
            "vest": "short sleeve top",
            "vest dress": "short sleeve top"
        }

        lower_mapping = {
            "long sleeve dress": "skirt",
            "short sleeve dress": "skirt",
            "sling": "skirt",
            "sling dress": "skirt",
            "vest": "skirt",
            "vest dress": "skirt"
        }

        if is_upper:
            return upper_mapping.get(label, label)
        return lower_mapping.get(label, label)