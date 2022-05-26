import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class Util:

    # expects data in a form, where the class is always the last row
    @staticmethod
    def splitClasses(data) -> list:
        positiveClasses = []
        negativeClasses = []
        splitData = []

        # split data in classes for easier calculations in the cqql classifier
        for i in range(len(data) - 1):
            if data[i][data[0].shape[0] - 1] == 1:
                positiveClasses.append(data[i])
            else:
                negativeClasses.append(data[i])

        splitData.append(positiveClasses)
        splitData.append(negativeClasses)

        return splitData

    # normalizes dataset, so that each value is in the interval[0,1]
    # takes in a Matrix where each row represents the attribute and the column the attribute values an object has
    @staticmethod
    def normalizeDataset(matrix):
        scaler = MinMaxScaler(feature_range=(0, 1))
        normedMatrix = scaler.fit_transform(matrix)
        return normedMatrix
