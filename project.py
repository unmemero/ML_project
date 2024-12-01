from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV file
def getData():
    return pd.read_csv('./heart.csv')

# Drop rows with missing values4
def dropMissingValues(data):
    return data.dropna()

# Fill missing values with the mean of the column
def fillMissingValues(data):
    return data.fillna(data.mean())

# Convert data to sets for training and testing
def splitData(data):
    data = data.to_numpy()
    X = data[:, :-1]
    y = data[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0., random_state=0)
    return X_train, X_test, y_train, y_test

# Print metrics
def printMetrics(y_test, y_pred):
    print('F1 score:', f1_score(y_test, y_pred))
    print('Confusion matrix:', confusion_matrix(y_test, y_pred))
    print('Accuracy:', accuracy_score(y_test, y_pred))
    print('Recall:', recall_score(y_test, y_pred))
    print('Precision:', precision_score(y_test, y_pred))

# W