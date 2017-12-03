import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import random
import numpy as np
from Tkinter import *

'''This module contains the functionality to perform the user rating prediction analysis'''

'''Print each of the correlations'''
'''Print the MLP Score'''


def calculate(frame, data):
    # create list of budget, user_rating, runtimes, release year and cast fb likes for correlation analysis
    budget = []
    user = []
    fb_likes = []
    runtime = []
    release = []

    for pt in data:
        budget.append(pt.budget)
        user.append(pt.rating)
        fb_likes.append(pt.fb_likes)
        runtime.append(pt.runtime)
        release.append(pt.release)

    # Calculate correlations among numerical data types
    p_fb_likes = pearsonr(fb_likes, user)
    p_budget = pearsonr(budget, user)
    p_runtime = pearsonr(runtime, user)
    p_release = pearsonr(release, user)

    s_fb_likes = spearmanr(fb_likes, user)
    s_budget = spearmanr(budget, user)
    s_runtime = spearmanr(runtime, user)
    s_release = spearmanr(release, user)

    # set up mlp to perform user rating prediction
    mlp = MLPRegressor(hidden_layer_sizes=(20, 20), activation='tanh', solver='adam', max_iter=500, verbose=True)

    data_pts = data
    random.shuffle(data_pts)
    data_array = np.array(data_pts)

    X = data_array[:, 0:-1]
    Y = data_array[:, -1]
    cut = int(0.66*len(X))

    # Scale data to avoid network saturation
    X_train = X[:cut]
    X_test = X[cut:]
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    mlp.fit(X_train, Y[:cut])
    mlp_score = mlp.score(X_test, Y[cut:])

    # Print results to screen
    frame.text.insert(INSERT, "Correlation Results:\nCast Facebook Likes & User Rating, Pearson: %.2f; Spearman: %.2f\n"
                              "Budget and User Rating, Pearson: %.2f; Spearman: %.2f\n"
                              "Runtime and User Rating, Pearson: %.2f; Spearman: %.2f\n"
                              "Release Year and User Rating, Pearson: %.2f; Spearman: %.2f\n"
                              "\nNeural Network R^2 Score: %.2f\n"
                              "\n"
                      % (p_fb_likes[0], s_fb_likes[0], p_budget[0], s_budget[0], p_runtime[0], s_runtime[0],
                         p_release[0], s_release[0], mlp_score))

    # Send plot of top revenue earning genre probability distributions to GUI
    frame.ax.scatter(release, user)
    frame.ax.set_title("Release Year vs. User Rating")
    frame.ax.set_xlabel('Release Year')
    frame.ax.set_ylabel('User Rating')







