from sklearn.neighbors.kde import KernelDensity
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
import collections

'''Print pre_user_rating_stat'''
'''Print post_user_rating_stat'''

def calculate(data):
    genre_user = data.user_rating
    genre_fb = data.fb_likes
    instances = data.pts

    pre_user = collections.defaultdict(list)
    post_user = collections.defaultdict(list)
    for pt in instances:
        if pt[3] < 1990:
            pre_user[pt[0]].append(float(pt[1]))
        else:
            post_user[pt[0]].append(float(pt[1]))

    # Calculate summary statistics for each genre
    stat = collections.namedtuple('stat', ('mean', 'min', 'max', 'stdev', 'count'))

    pre_user_rating_stat = {}  # User rating statistics during early era
    for key in pre_user.keys():
        pre_user_rating_stat[key] = stat(np.mean(pre_user[key]), np.min(pre_user[key]),
                                              np.max(pre_user[key]), np.std(pre_user[key]), len(pre_user[key]))

    print(pre_user_rating_stat)

    post_user_rating_stat = {}  # User rating statistics during later era
    for key in post_user.keys():
        post_user_rating_stat[key] = stat(np.mean(post_user[key]), np.min(post_user[key]), np.max(post_user[key]),
                                          np.std(post_user[key]), len(post_user[key]))

    print(post_user_rating_stat)

    # Calculate user rating probability distribution or each genre during early era
    pre_distributions = {}
    for key in pre_user.keys():
        X = pre_user[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 10, 100)

        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        pre_distributions[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()

    # Calculate user rating probability distribution for each genre during late eras
    post_distributions = {}
    for key in post_user.keys():
        X = post_user[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 10, 100)

        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        post_distributions[key] = log_pdf

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

        kde = KernelDensity(kernel='gaussian', bandwidth=0.1).fit(X)
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




