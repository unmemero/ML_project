# Model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

class Model:
    """Encapsulates the Model functionality."""

    def __init__(self):
        """Initialize the Model with the dataset and train the model."""
        self.dataset = None
        self.X = None
        self.y = None
        self.feature_names = None
        self.class_names = None
        self.classifier = None

        # Load the dataset and train the model
        self.load_dataset('data/heart.csv')  # Update with your dataset path
        self.train_model()

    def load_dataset(self, file_path):
        """
        Load the dataset from a CSV file.

        :param file_path: Path to the CSV file.
        """
        self.dataset = pd.read_csv(file_path)
        self.X = self.dataset.iloc[:, :-1]
        self.y = self.dataset.iloc[:, -1]
        self.feature_names = self.X.columns.tolist()
        self.class_names = self.y.unique()

    def train_model(self):
        """Train a DecisionTreeClassifier model."""
        self.classifier = DecisionTreeClassifier(random_state=1, max_depth=9)
        self.classifier.fit(self.X, self.y)

    def predict(self, X):
        """
        Predict the class labels for the provided data.

        :param X: Input data to predict.
        :return: Predicted class labels.
        """
        return self.classifier.predict(X)

    def get_feature_names(self):
        """Get the feature names used in the model."""
        return self.feature_names

    def get_class_names(self):
        """Get the class names used in the model."""
        return self.class_names

    def get_classifier(self):
        """Get the trained classifier model."""
        return self.classifier

    def split_data(self, test_size=0.2):
        """
        Split the dataset into training and testing sets.

        :param test_size: Fraction of the dataset to include in the test split.
        """
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=1
        )
        return X_train, X_test, y_train, y_test