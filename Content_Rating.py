import numpy as np
import collections
from sklearn.neighbors.kde import KernelDensity
import matplotlib.pyplot as plt


def calculate(data):
    # Calculate revenue probability distribution for each rating
    rating_revenue_dist = {}
    for key in data.revenue.keys():
        X = data.budget[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 309404152, 100000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        rating_revenue_dist[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()

    # Calculate budget probability distribution for each rating
    rating_budget_dist = {}
    for key in data.budget.keys():
        X = data.budget[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 309404152, 100000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        rating_budget_dist[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()

    # Calculate summary statistics for common ratings (G, PG, PG-13, R)
    stat = collections.namedtuple('stat', ('mean', 'min', 'max', 'stdev'))

    rating_budget_stat = {}
    for key in data.budget.keys():
        rating_budget_stat[key] = stat(np.mean(data.budget[key]), np.min(data.budget[key]), np.max(data.budget[key]),
                                      np.std(data.budget[key]))

    