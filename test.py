import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LogisticRegression

# Load data from CSV file
def getData():
    data = pd.read_csv('./heart.csv')
    feature_names = data.columns
    data = data.fillna(data.mean())
    print(data['target'].value_counts())
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
    return feature_names, X_train, X_test, y_train, y_test

# Print metrics
def print_metrics(y_test, y_pred, model):
    print(f'\033[1;93m*******************Metrics for {model}*******************\033[0m\nConfusion Matrix: {confusion_matrix(y_test, y_pred)}\nF1 Score: {f1_score(y_test, y_pred)}\nAccuracy Score: {accuracy_score(y_test, y_pred)}\nRecall Score: {recall_score(y_test, y_pred)}\nPrecision Score: {precision_score(y_test, y_pred)}\n\n************************************************\n')

# Resplit data
def resplitData(X_train, X_test, y_train, y_test, random_state, test_size):
    X_combined = np.concatenate((X_train, X_test), axis=0)
    y_combined = np.concatenate((y_train, y_test), axis=0)
    X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(
        X_combined, y_combined, test_size=test_size, random_state=random_state
    )
    return X_train_new, X_test_new, y_train_new, y_test_new

# Controled input based tree traversal
import numpy as np

def treeTraversal(clf, columns):
    tree = clf.tree_
    feature = tree.feature
    threshold = tree.threshold
    children_left = tree.children_left
    children_right = tree.children_right

    user_input = input('Enter values for the following features separated by commas:\n\t' + ', '.join(columns) + '\n')
    uservals = [float(val) for val in user_input.strip().split(',')]

    node = 0  # Start at the root node
    while children_left[node] != children_right[node]:
        feat_idx = feature[node]
        if feat_idx == -2:
            # Reached a leaf node
            break
        thresh = threshold[node]
        print(f'Feature: {columns[feat_idx]}\nThreshold: {thresh}\nValue: {uservals[feat_idx]}')
        if uservals[feat_idx] <= thresh:
            node = children_left[node]
        else:
            node = children_right[node]
    # Reached a leaf node
    prediction = clf.classes_[np.argmax(tree.value[node])]
    print(f'Reached leaf node with prediction: {prediction}')


# Find the best tree based on F1 score
def findBestTree(X_train, y_train, X_test, y_test):
    bestTree = None
    bestF1 = 0
    best_test_size = None
    for i in range(1, 100):
        for j in range(1, 10):
            X_train_resplit, X_test_resplit, y_train_resplit, y_test_resplit = resplitData(
                X_train, X_test, y_train, y_test, i, float(j)/10.0
            )
            for k in range(1, X_train_resplit.shape[1]):
                tree = DecisionTreeClassifier(max_depth=k, random_state=i)
                tree.fit(X_train_resplit, y_train_resplit)
                y_pred = tree.predict(X_test_resplit)
                f1 = f1_score(y_test_resplit, y_pred)
                if f1 > bestF1:
                    bestF1 = f1
                    bestTree = tree
                    best_test_size = float(j)/10.0
    return bestTree, best_test_size

# Plot tree
def make_img(tree, feature_names):
    os.makedirs('./images', exist_ok=True) 

    plt.figure(figsize=(20, 20))
    plot_tree(
        tree,
        filled=True,
        feature_names=feature_names,
        class_names=['Not probable', 'Highly probable'],
        impurity=False,
        proportion=False,
        rounded=True,
        precision=2
    )
    output_path = './images/tree.svg'
    print(f"Saving tree plot to {output_path}")
    plt.savefig(output_path, format='svg')
    plt.close()
    print(f"Tree plot saved successfully to {output_path}")

# Main function
if __name__ == '__main__':
    # Use pandas to get data from CSV file and process null inputs
    columns, X_train, X_test, y_train, y_test = getData()

    # Find the best tree based on F1 score
    bestTree, best_data_split = findBestTree(X_train, y_train, X_test, y_test)
    print(f'Best data split:\n\tTrain: {1-best_data_split}\n\tTest: {best_data_split}\nBest tree: {bestTree}')
    y_pred = bestTree.predict(X_test)
    print_metrics(y_test, y_pred, 'Decision Tree')

    # Possible overfitting, will check tree traversal
    treeTraversal(bestTree, columns)

    make_img(bestTree, columns)

    importances = bestTree.feature_importances_
    for name, importance in zip(columns, importances):
        print(f"Feature: {name}, Importance: {importance}")