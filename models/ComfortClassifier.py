import pandas as pd
from sklearn.ensemble import RandomForestClassifier


class ComfortClassifier:
    def __init__(self):
        # self.classifier = CatBoostClassifier(iterations=100, learning_rate=0.1, depth=5)
        self.classifier = RandomForestClassifier()
        self.ds = pd.read_csv("models/data.csv")
        self.columns = self.ds.columns[:-1]
        self.train_classifier()

    def train_classifier(self):
        X_train = self.ds.drop("comfort_level", axis=1)
        y_train = self.ds["comfort_level"]
        self.classifier.fit(X_train, y_train)

    def predict_comfort_level(self, labels: list[tuple], local_temp: float, local_humid: float):
        input_data = []
        for upper_label, lower_label in labels:
            row_data = [0] * len(self.columns)
            if upper_label:
                row_data[self.columns.get_loc(upper_label)] = 1
            if lower_label:
                row_data[self.columns.get_loc(lower_label)] = 1
            row_data[-2] = local_temp
            row_data[-1] = local_humid
            input_data.append(row_data)

        input_df = pd.DataFrame(input_data, columns=self.columns)
        comfort_levels = self.classifier.predict(input_df)
        return comfort_levels.tolist()
