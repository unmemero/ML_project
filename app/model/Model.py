# Model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

"""
- Class to contain the model and its operations
- Mode and data split parameters based upon ../testing/test.py
- The model is trained using DecisionTreeClassifier with tested parameters (random_state=1, max_depth=9)
- The model is trained using the heart.csv dataset
"""

class Model:

    # Model constructor
    def __init__(self):
        self.dataset = None
        self.X = None
        self.y = None
        self.feature_names = None
        self.class_names = None
        self.classifier = None
        self.load_dataset('data/heart.csv') 
        self.train_model()

    # Load the dataset from heart.csv
    def load_dataset(self, file_path):
        self.dataset = pd.read_csv(file_path)
        self.dataset = self.dataset.fillna(self.dataset.mean())
        self.X = self.dataset.iloc[:, :-1]
        self.y = self.dataset.iloc[:, -1]
        self.feature_names = self.X.columns.tolist()
        self.class_names = self.y.unique()

    # Train the model using DecisionTreeClassifier with tessted parameters
    def train_model(self):
        self.classifier = DecisionTreeClassifier(random_state=1, max_depth=9)
        self.classifier.fit(self.X, self.y)

    # Return tree predictions from training data
    def predict(self, X):
        return self.classifier.predict(X)

    # Extract feature names from the dataset to use with GUI
    def get_feature_names(self):
        return self.feature_names

    # Extract class names from the dataset to use with GUI
    def get_class_names(self):
        return self.class_names

    # Return the model
    def get_classifier(self):
        return self.classifier

    # Split the data into training and testing sets
    def split_data(self, test_size=0.1):
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=1
        )
        return X_train, X_test, y_train, y_test