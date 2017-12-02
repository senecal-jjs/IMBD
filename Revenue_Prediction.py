import numpy as np
import random
import collections
from operator import itemgetter
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.neighbors.kde import KernelDensity
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn import datasets

'''This module contains the functionality to perfrom the revenue prediction analysis'''

'''Print each of the correlations'''
'''Print the logistic regression and mlp score'''


def calculate(data):
    numerical_data = data[0]     # fb_likes, budget, revenue, release year, runtime
    categorical_data = data[1]   # revenues associated with each genre

    # Calculate correlations among numerical data types
    p_fb_likes = pearsonr(numerical_data.fb_likes, numerical_data.revenue)
    p_budget = pearsonr(numerical_data.budget, numerical_data.revenue)
    p_release = pearsonr(numerical_data.release, numerical_data.revenue)
    p_runtime = pearsonr(numerical_data.runtime, numerical_data.revenue)

    s_fb_likes = spearmanr(numerical_data.fb_likes, numerical_data.revenue)
    s_budget = spearmanr(numerical_data.budget, numerical_data.revenue)
    s_release = spearmanr(numerical_data.budget, numerical_data.revenue)
    s_runtime = spearmanr(numerical_data.runtime, numerical_data.revenue)

    # Revenue class prediction with logistic regression
    data_pt = collections.namedtuple('data_pt', ('budget', 'fb_likes', 'revenue', 'release', 'runtime'))

    associated_data = []
    for i in range(len(numerical_data.budget)):
        associated_data.append(data_pt(numerical_data.budget[i], numerical_data.fb_likes[i], numerical_data.revenue[i],
                                       numerical_data.release[i], numerical_data.runtime[i]))

    # Create revenue classes
    sorted_revenue = sorted(associated_data, key=itemgetter(2))

    index1 = int(len(sorted_revenue)/4)
    index2 = index1*2
    index3 = index1*3
    class1 = sorted_revenue[:index1]
    class2 = sorted_revenue[index1:index2]
    class3 = sorted_revenue[index2:index3]
    class4 = sorted_revenue[index3:]

    # Assign class labels to the data
    labeled_data = []
    for instance in class1:
        labeled_data.append(([instance.budget, instance.fb_likes, instance.release, instance.runtime], 0))

    for instance in class2:
        labeled_data.append(([instance.budget, instance.fb_likes, instance.release, instance.runtime], 1))

    for instance in class3:
        labeled_data.append(([instance.budget, instance.fb_likes, instance.release, instance.runtime], 2))

    for instance in class4:
        labeled_data.append(([instance.budget, instance.fb_likes, instance.release, instance.runtime], 3))

    # Assign data to training and testing sets
    cut = int(0.66 * len(sorted_revenue))
    random.shuffle(labeled_data)
    training_data = labeled_data[:cut]
    testing_data = labeled_data[cut:]

    # Separate data and targets
    X = []
    Y = []
    for instance in training_data:
        X.append(instance[0])
        Y.append(instance[1])

    X = np.array(X)
    Y = np.array(Y)

    model = LogisticRegression()
    model.fit(X, Y)

    # Separate testing data
    Xt =[]
    Yt = []
    for instance in testing_data:
        Xt.append(instance[0])
        Yt.append(instance[1])

    print("Logistic Regression score: %s" % model.score(Xt, Yt))

    mlp = MLPClassifier(hidden_layer_sizes=(30, 30), activation='tanh', max_iter = 500, verbose=True, shuffle=True)
    mlp.fit(X, Y)
    print("MLP Score: %s" % mlp.score(Xt, Yt))

    # Calculate probability distribution for each genre
    distributions = {}
    for key in categorical_data.keys():
        X = categorical_data[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 309404152, 100000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        distributions[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()



