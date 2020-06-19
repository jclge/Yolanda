from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn import datasets
from sklearn import metrics
import pandas as pd
import sys

def get_dataset(set):
    data = pd.read_csv(set, delimiter=',')
    tuples = [tuple(y) for y in data.values]
    # print (tuples)
    return (tuples)

def main(av):
    tuples = get_dataset(av[1])
    nparray = np.array(tuples, dtype=None, copy=True, order='K', subok=False, ndmin=0)
    analysis = np.array([1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0], dtype=None, copy=True, order='K', subok=False, ndmin=0)
    K = 3
    model = KNeighborsClassifier(n_neighbors = K)
    model.fit(nparray, analysis)
    print(model)
    print(model.predict([[43.89796442411784,4.158567154102174,1.5890451532845034,0.3941704599110927,17.860141026637645,24.64694971323936,5.437138850020729,8.799117836742214]]))

if __name__ == "__main__":
    main(sys.argv)


# import pandas as pd
# from pandas import read_csv
# from pandas.plotting import scatter_matrix
# from matplotlib import pyplot
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn import metrics
# import numpy as np
# import graphviz
# from sklearn.tree import export_graphviz
# import pydot

# df = pd.read_csv("max.csv")
# print(df.shape)
# print(df.describe())
# #features = pd.get_dummies(df)
# #labels = np.array(features)
# #feature_list = list(features.columns)
# #features = np.array(features)
# features = df.iloc[:, 0:4].values
# labels = df.iloc[:, 4].values
# train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, random_state = 0)
# print('Training Features Shape:', train_features.shape)
# print('Training Labels Shape:', train_labels.shape)
# print('Testing Features Shape:', test_features.shape)
# print('Testing Labels Shape:', test_labels.shape)
# rf = RandomForestRegressor(n_estimators = 20, random_state = 0)
# rf.fit(train_features, train_labels)
# predictions = rf.predict(test_features)
# errors = abs(predictions - test_labels)
# print('Mean Absolute Error:', metrics.mean_absolute_error(test_features, predictions))
# print('Mean Absolute Error:', round(np.mean(errors), 2))