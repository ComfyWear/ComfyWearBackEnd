"""The module containing the classifier for inference the comfort level."""
import os
from typing import List, Tuple
import joblib
import pandas as pd
import numpy as np

from utils import check_and_download_files


class ComfortClassifier:
    """Classifier for inferring comfort level based on environmental."""
    def __init__(self):
        self.model_base_path = "models/weights/"
        check_and_download_files(self.model_base_path)
        self.resource_path = "models/model_resources/data.csv"
        self.columns = pd.read_csv(self.resource_path).columns[:-1]
        self.classifier = self.load_model(os.path.join(self.model_base_path,
                                                       "gb_model.pkl"))
        self.scaler_temp_humid = self.load_model(os.path.join(
            self.model_base_path, "scaler_temp_humid.pkl"))
        self.scaler_other = self.load_model(os.path.join(self.model_base_path,
                                                         "scaler_other.pkl"))

    def load_model(self, path):
        """
        Load a joblib model file with error handling for compatibility issues.
        """
        try:
            return joblib.load(path)
        except KeyError as e:
            print(f"Failed to load the model due to a KeyError: {e}. "
                  "This might be caused by a Python version mismatch.")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def predict_comfort_level(self, labels: List[Tuple], local_temp: float,
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
        print("Input data:")
        print(input_df)
        comfort_levels: np.ndarray = self.classifier.predict(input_df)
        print("Comfort levels:")
        print(comfort_levels)
        return comfort_levels.tolist()

    def _prepare_input_data(self, labels: List[Tuple], local_temp: float,
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
        input_cloth: list = []
        input_temp_humid: list = []
        for upper_label, lower_label in labels:
            row_cloth: list = [0] * (len(self.columns) - 2)
            row_temp_humid: list = [0] * 2
            if upper_label:
                upper_label = self._map_input(upper_label)
                row_cloth[self.columns.get_loc(upper_label)] = 1
            if lower_label:
                lower_label = self._map_input(lower_label, False)
                row_cloth[self.columns.get_loc(lower_label)] = 1

            row_temp_humid[0] = local_temp
            row_temp_humid[1] = local_humid
            input_cloth.append(row_cloth)
            input_temp_humid.append(row_temp_humid)

        X_temp_humid = self.scaler_temp_humid.transform(input_temp_humid)
        X_other = self.scaler_other.transform(input_cloth)

        return np.concatenate((X_temp_humid, X_other), axis=1)

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