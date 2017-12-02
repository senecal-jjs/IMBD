from sklearn.neighbors.kde import KernelDensity
import numpy as np
import collections
import matplotlib.pyplot as plt


def calculate(data):
    # Calculate summary statistics for common ratings (G, PG, PG-13, R)
    stat = collections.namedtuple('stat', ('mean', 'min', 'max', 'stdev', 'count'))

    rating_runtime_stat = {}  # Budget Statistics associated with each rating
    for key in data.content.keys():
        rating_runtime_stat[key] = stat(np.mean(data.content[key]), np.min(data.content[key]), np.max(data.content[key]),
                                       np.std(data.content[key]), len(data.content[key]))

    print(rating_runtime_stat)

    genre_runtime_stat = {}  # Revenue statistics associated with each rating
    for key in data.genre.keys():
        genre_runtime_stat[key] = stat(np.mean(data.genre[key]), np.min(data.genre[key]), np.max(data.genre[key]),
                                       np.std(data.genre[key]), len(data.genre[key]))

    # Calculate runtime probability distribution for each genre
    genre_runtime_dist = {}
    for key in data.genre.keys():
        X = data.genre[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 200, 200)

        kde = KernelDensity(kernel='gaussian', bandwidth=10).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        genre_runtime_dist[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()

    # Calculate runtime probability distribution for each rating
    rating_runtime_dist = {}
    for key in data.content.keys():
        X = data.content[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 200, 200)

        kde = KernelDensity(kernel='gaussian', bandwidth=10).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        rating_runtime_dist[key] = log_pdf

        plt.plot(x_grid, np.exp(log_pdf))
        plt.title(key)
        plt.show()
