import numpy as np
import random
import collections
from operator import itemgetter
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.neighbors.kde import KernelDensity
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from Tkinter import *
import matplotlib.pyplot as plt
import os

'''This module contains the functionality to perfrom the revenue prediction analysis'''

'''Print each of the correlations'''
'''Print the logistic regression and mlp score'''


def calculate(frame, data):
    numerical_data = data[0]     # fb_likes, budget, revenue, release year, runtime
    categorical_data = data[1]   # revenues associated with each genre

    # Calculate revenue summary statistics for the Genres
    stat = collections.namedtuple('stat', ('mean', 'min', 'max', 'stdev'))

    genre_revenue_stat = {}  # Revenue Statistics associated with each genre
    for key in categorical_data.keys():
        genre_revenue_stat[key] = stat(round(np.mean(categorical_data[key]), 2), round(np.min(categorical_data[key]), 2),
                                       round(np.max(categorical_data[key]), 2), round(np.std(categorical_data[key]), 2))

    print(sorted(genre_revenue_stat, key=lambda k: genre_revenue_stat[k][0]))

    # Calculate correlations among numerical data types
    p_fb_likes = pearsonr(numerical_data.fb_likes, numerical_data.revenue)
    p_budget = pearsonr(numerical_data.budget, numerical_data.revenue)
    p_release = pearsonr(numerical_data.release, numerical_data.revenue)
    p_runtime = pearsonr(numerical_data.runtime, numerical_data.revenue)

    s_fb_likes = spearmanr(numerical_data.fb_likes, numerical_data.revenue)
    s_budget = spearmanr(numerical_data.budget, numerical_data.revenue)
    s_release = spearmanr(numerical_data.release, numerical_data.revenue)
    s_runtime = spearmanr(numerical_data.runtime, numerical_data.revenue)

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

    log_score = model.score(Xt, Yt)

    mlp = MLPClassifier(hidden_layer_sizes=(30, 30), activation='tanh', max_iter = 500, verbose=False, shuffle=True)
    mlp.fit(X, Y)
    mlp_score = mlp.score(Xt, Yt)

    # Print results to screen
    frame.text.insert(INSERT, "Correlation Results:\nCast Facebook Likes & Revenue, Pearson: %.2f; Spearman: %.2f\n"
                              "Budget and Revenue, Pearson: %.2f; Spearman: %.2f\n"
                              "Release Year and Revenue, Pearson: %.2f; Spearman: %.2f\n"
                              "Runtime and Revenue, Pearson: %.2f; Spearman: %.2f\n"
                              "\nLogistic Regression Classification Accuracy: %.2f\n"
                              "\nNeural Network Classification Accuracy: %.2f\n"
                              "\n"
                      % (p_fb_likes[0], s_fb_likes[0], p_budget[0], s_budget[0], p_release[0], s_release[0],
                         p_runtime[0], s_runtime[0], log_score, mlp_score))

    for key in genre_revenue_stat.keys():
        frame.text.insert(END, "\n" + str(key) + ": " + str(genre_revenue_stat[key]) + "\n")

    # Calculate probability distribution for each genre
    distributions = {}
    for key in categorical_data.keys():
        X = categorical_data[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 309404152, 100000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        distributions[key] = np.exp(log_pdf)

        frame.ax.plot(x_grid, np.exp(log_pdf))
        frame.ax.set_title(str(key) + " Revenue Probability Distribution")
        frame.ax.set_xlabel("Revenue (USD)")
        frame.ax.set_ylabel("Probability")

        frame.f.savefig("Plots/" + str(key) + "_revenue_dist")
        frame.ax.cla()

    # Save correlation plots to file
    frame.ax.scatter(numerical_data.budget, numerical_data.revenue)
    frame.ax.set_title("Budget vs Revenue")
    frame.ax.set_xlabel("Budget (USD)")
    frame.ax.set_ylabel("Revenue (USD)")
    frame.f.savefig("Plots/_budget_revenue_corr")
    frame.ax.cla()

    frame.ax.scatter(numerical_data.fb_likes, numerical_data.revenue)
    frame.ax.set_title("Cast Facebook Likes vs Revenue")
    frame.ax.set_xlabel("Cast Facebook Likes")
    frame.ax.set_ylabel("Revenue (USD)")
    frame.f.savefig("Plots/_cast_fb_likes_revenue_corr")
    frame.ax.cla()

    frame.ax.scatter(numerical_data.release, numerical_data.revenue)
    frame.ax.set_title("Release Year vs Revenue")
    frame.ax.set_xlabel("Release Year")
    frame.ax.set_ylabel("Revenue (USD)")
    frame.f.savefig("Plots/_release_year_revenue_corr")
    frame.ax.cla()

    frame.ax.scatter(numerical_data.runtime, numerical_data.revenue)
    frame.ax.set_title("Runtime vs Revenue")
    frame.ax.set_xlabel("Runtime (min)")
    frame.ax.set_ylabel("Revenue (USD)")
    frame.f.savefig("Plots/_runtime_revenue_corr")
    frame.ax.cla()

    # Save bar charts of mean revenue
    means = []
    stdev = []
    names = []

    for key in genre_revenue_stat.keys():
        if key == "Sci-Fi" or key == "Family" or key == "Adventure" or key == "Animation":
            means.append(genre_revenue_stat[key].mean)
            stdev.append(genre_revenue_stat[key].stdev)
            names.append(key)

    ind = np.arange(len(means))
    frame.ax.set_ylabel('Revenue (USD)')
    frame.ax.set_title('Revenue by Genre')
    frame.ax.set_xticks([p + 0.2 for p in ind])
    frame.ax.set_xticklabels(names)
    frame.ax.bar(ind, means, width = 0.5)
    frame.f.savefig("Plots/bar_genre_revenue")
    frame.ax.cla()

    # Send plot of top revenue earning genre probability distributions to GUI
    frame.ax.plot(x_grid, distributions['Animation'], label="Animation")
    frame.ax.plot(x_grid, distributions['Family'], label="Family")
    frame.ax.plot(x_grid, distributions['Adventure'], label="Adventure")
    frame.ax.plot(x_grid, distributions['Sci-Fi'], label="Sci-Fi")
    frame.ax.set_title("Probability Dist. for Top Revenue Earning Genres")
    frame.ax.set_xlabel('Revenue (USD)')
    frame.ax.set_ylabel('Probability')

    handles, labels = frame.ax.get_legend_handles_labels()
    frame.ax.legend(handles, labels)


