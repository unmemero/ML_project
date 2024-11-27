import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score, recall_score, precision_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# Load data from CSV file
def getData():
    return pd.read_csv('./heart.csv')
# Drop rows with missing values
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
    X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.5, shuffle=True)
    return X_train, X_test, y_train, y_test

def findBestTree(X_train, y_train, X_test, y_test):
    bestTree = None
    bestF1 = 0
    for i in range(1, 100):
        tree = DecisionTreeClassifier(max_depth=i)
        tree.fit(X_train, y_train)
        y_pred = tree.predict(X_test)
        f1 = f1_score(y_test, y_pred)
        if f1 > bestF1:
            bestF1 = f1
            bestTree = tree
    return bestTree

#Plot tree
def plotTree(tree, feature_names):
    plt.figure(figsize=(20, 20))
    plot_tree(tree, filled=True, feature_names=feature_names, class_names=['Not probable', 'Highly probable'], impurity=False, proportion=False, rounded=True, precision=2)
    plt.savefig('tree.svg', format='svg')

if __name__ == '__main__':
    data = getData()
    dropMissingValues(data)
    fillMissingValues(data)
    X_train, y_train, X_test, y_test = splitData(data)
    bestTree = findBestTree(X_train, y_train, X_test, y_test)
    print(bestTree)
    y_pred = bestTree.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    print(f'F1 Score: {f1_score(y_test, y_pred)}')
    print(f'Accuracy Score: {accuracy_score(y_test, y_pred)}')
    print(f'Recall Score: {recall_score(y_test, y_pred)}')
    print(f'Precision Score: {precision_score(y_test, y_pred)}')
    print()
    feature_importances = bestTree.feature_importances_
    features = data.columns[:-1]
    feature_importance_dict = dict(zip(features, feature_importances))
    sorted_features = sorted(feature_importance_dict.items(), key=lambda item: item[1], reverse=True)
    print("Feature importances:")
    for feature, importance in sorted_features:
        print(f"{feature}: {importance}")

    plotTree(bestTree, feature_names=features)