import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


class Knn:

    def __init__(self, k):
        self.neighbours_num = k
        self.data_set = None
        self.labels = None

    def fit(self, x_data_set, y_labels):
        """

        :param x_data_set:
        :param y_labels:
        :return:
        """
        self.data_set = x_data_set
        self.labels = y_labels

    def predict(self, x):
        """

        :param x:
        :return:
        """
        count_1_labels = 0
        count_0_labels = 0
        distance = {}

        # calculate all the distances
        for (i, x_vec) in enumerate(self.data_set):
            distance[i] = np.linalg.norm(x-x_vec)

        sorted_distance = sorted(distance.keys(), key=lambda t: distance[t])

        # find the k-smallest x's and check their  labels
        for j in range(self.neighbours_num):
            if y_train_labels[sorted_distance[j]] == 1:
                count_1_labels += 1
            else:
                count_0_labels += 1

        if count_1_labels > count_0_labels:
            return 1
        else:
            return 0


def logic_regression_errors(x_test, y_test_labels, x_train, y_train_labels, test_length):
    """

    :return:
    """
    logistic_errors = 0
    logistic_r.fit(x_train, y_train_labels)
    predict = logistic_r.predict(x_test)
    for index, value in enumerate(predict):
        if value != y_test_labels[index]:
            logistic_errors += 1
    return (float(logistic_errors)/ test_length)

def partition_data():
    """

    :param data_path:
    :return:
    """
    df = pd.read_csv((r"spam_data.csv"))
    labels = df['57'].to_numpy()
    df = df.drop(labels='57', axis=1).to_numpy()
    random = np.random.choice(len(df), len(df), replace=False)
    train_data_samples = df[random[1000:]]
    train_data_labels = labels[random[1000:]]
    test_data_samples = df[random[:1000]]
    test_data_labels = labels[random[:1000]]
    return train_data_samples, train_data_labels, test_data_samples, test_data_labels


if __name__ == '__main__':

    k_vals = [1, 2, 5, 10, 100]
    error_rate = [0,0,0,0,0]
    logistic_r = LogisticRegression()

    x_train , y_train_labels, x_test, y_test_labels = partition_data()

    test_length = len(x_test)

    log_reg_err_avg = 0

    # calculating the y_labels for the test samples and the train samples

    for index in range(len(k_vals)):
        knn_errors = 0

        knn = Knn(k_vals[index])
        knn.fit(x_train, y_train_labels)

        for i in range(test_length):
            if knn.predict(x_test[i]) != y_test_labels[i]:
                knn_errors += 1

        error_rate[index] += knn_errors / test_length

    log_reg_err_avg = logic_regression_errors(x_test, y_test_labels, x_train, y_train_labels, test_length)

    for l in range(5):
        print(
            "k=%d test error is: %lf" % (k_vals[l], error_rate[l]))
    print(
        "logistic regression test error is: %lf" % log_reg_err_avg)
