from sklearn.neighbors.kde import KernelDensity
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
import collections


def calculate(data):
    genre_user = data.user_rating
    genre_fb = data.fb_likes
    instances = data.pts

    pre_2000_user = collections.defaultdict(list)
    post_2000_user = collections.defaultdict(list)
    for pt in instances:
        if pt[3] < 2000:
            pre_2000_user[pt[0]].append(float(pt[1]))
        else:
            post_2000_user[pt[0]].append(float(pt[1]))

    # Calculate user rating probability distribution or each genre during different eras
    pre_2000_distributions = {}
    for key in pre_2000_user.keys():
        X = pre_2000_user[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 10, 100)

        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        pre_2000_distributions[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()

    # Calculate user rating probability distribution or each genre during different eras
    post_2000_distributions = {}
    for key in post_2000_user.keys():
        X = post_2000_user[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 10, 100)

        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        post_2000_distributions[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()


    # Calculate user rating probability distribution for each genre
    user_distributions = {}
    for key in genre_user.keys():
        X = genre_user[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 10, 100)

        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        user_distributions[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()

    # Calculate facebook likes probability distribution for each genre
    fb_distributions = {}
    for key in genre_fb.keys():
        X = genre_fb[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 200000, 50000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        fb_distributions[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()




