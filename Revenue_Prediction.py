import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.neighbors.kde import KernelDensity


def calculate(data):
    numerical_data = data[0]     # fb_likes, budget, revenue
    categorical_data = data[1]   # revenues associated with each genre

    # Calculate correlations among numerical data types
    pearson_fb_likes = pearsonr(numerical_data.fb_likes, numerical_data.revenue)
    pearson_budget = pearsonr(numerical_data.budget, numerical_data.revenue)

    spearman_fb_likes = spearmanr(numerical_data.fb_likes, numerical_data.revenue)
    spearman_budget = spearmanr(numerical_data.budget, numerical_data.revenue)

    # Calculate probability distribution for each genre
    print(categorical_data.keys())

    distributions = {}
    for key in categorical_data.keys():
        X = categorical_data[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 309404152, 100000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        distributions[key] = log_pdf

        # plt.plot(x_grid, np.exp(log_pdf))
        # plt.show()



