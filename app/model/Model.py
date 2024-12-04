import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

class Model:
    # Model constructor
    def __init__(self):
        self.dataset = None
        self.X = None
        self.y = None
        self.feature_names = None
        self.class_names = None
        self.classifier = None
        self.load_dataset(self.resource_path('data/heart.csv')) 
        self.train_model()

    # Resolve resource path for PyInstaller
    @staticmethod
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    # Load dataset from heart.csv
    def load_dataset(self, file_path):
        self.dataset = pd.read_csv(file_path)
        self.dataset = self.dataset.fillna(self.dataset.mean())
        self.X = self.dataset.iloc[:, :-1]
        self.y = self.dataset.iloc[:, -1]
        self.feature_names = self.X.columns.tolist()
        self.class_names = self.y.unique()

    # Train model using DST with test params from testing files
    def train_model(self):
        self.classifier = DecisionTreeClassifier(random_state=1, max_depth=9)
        self.classifier.fit(self.X, self.y)

    # Get predictions
    def predict(self, X):
        return self.classifier.predict(X)

    # Get feature names
    def get_feature_names(self):
        return self.feature_names

    # Extract class names from the dataset to use with GUI
    def get_class_names(self):
        return self.class_names

    # Return model
    def get_classifier(self):
        return self.classifier

    # Split data into training and testing
    def split_data(self, test_size=0.1):
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=1
        )
        return X_train, X_test, y_train, y_test
