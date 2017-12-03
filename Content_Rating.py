import numpy as np
import collections
from sklearn.neighbors.kde import KernelDensity
import matplotlib.lines as mlines
from Tkinter import *

'''Print the summary statistics in rating_budget_stat and rating_reveneue_stat'''


def calculate(frame, data):
    # Calculate summary statistics for common ratings (G, PG, PG-13, R)
    stat = collections.namedtuple('stat', ('mean', 'min', 'max', 'stdev', 'count'))

    rating_budget_stat = {}  # Budget Statistics associated with each rating
    for key in data.budget.keys():
        rating_budget_stat[key] = stat(np.mean(data.budget[key]), np.min(data.budget[key]), np.max(data.budget[key]),
                                       np.std(data.budget[key]), len(data.budget[key]))

    rating_revenue_stat = {} # Revenue statistics associated with each rating
    for key in data.revenue.keys():
        rating_revenue_stat[key] = stat(np.mean(data.revenue[key]), np.min(data.revenue[key]), np.max(data.revenue[key]),
                                        np.std(data.revenue[key]), len(data.budget[key]))

    # Calculate revenue probability distribution for each rating
    rating_revenue_dist = {}
    for key in data.revenue.keys():
        X = data.budget[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 309404152, 100000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        rating_revenue_dist[key] = np.exp(log_pdf)

    # Calculate budget probability distribution for each rating
    rating_budget_dist = {}
    for key in data.budget.keys():
        X = data.budget[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 309404152, 100000)

        kde = KernelDensity(kernel='gaussian', bandwidth=10000000).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        rating_budget_dist[key] = np.exp(log_pdf)

    # Print summary statistics to screen
    frame.text.insert(INSERT, "Content Rating Budget Stats:\n")
    for key in rating_budget_stat.keys():
        frame.text.insert(END, "\n" + str(key) + ": MEAN:" + str(rating_budget_stat[key].mean) + " STDEV: " + str(
            rating_budget_stat[key].stdev) + "\n")

    frame.text.insert(END, "\n\n\n\n\nContent Rating Revenue Stats:\n")
    for key in rating_revenue_stat.keys():
        frame.text.insert(END, "\n" + str(key) + ": MEAN:" + str(rating_revenue_stat[key].mean) + " STDEV: " + str(
            rating_revenue_stat[key].stdev) + "\n")

    # Create budget distributions
    frame.ax.plot(x_grid, rating_budget_dist['G'], label="G")
    frame.ax.plot(x_grid, rating_budget_dist['PG'], label="PG")
    frame.ax.plot(x_grid, rating_budget_dist['PG-13'], label="PG-13")
    frame.ax.plot(x_grid, rating_budget_dist['R'], label="R")
    frame.ax.set_title("Probability Dist. for Common Ratings")
    frame.ax.set_xlabel('Budget')
    frame.ax.set_ylabel('Probability')

    handles, labels = frame.ax.get_legend_handles_labels()
    frame.ax.legend(handles, labels)
    frame.ax.cla()

    # Create bubble chart of budget vs revenue, with bubbles representing the market share of the rating
    revenue = []
    budget = []
    size = []
    names = []
    for key in rating_budget_stat.keys():
        names.append(key)
        revenue.append(rating_revenue_stat[key].mean)
        budget.append(rating_budget_stat[key].mean)
        size.append(rating_budget_stat[key].count)

    rating_color = ['red', 'green', 'black', 'yellow', 'blue', 'orange', 'gray', 'magenta', 'lime', 'sienna', 'cyan', 'pink']

    size = [5*x for x in size]
    frame.ax.scatter(budget, revenue, s=size, c=rating_color)
    frame.ax.set_ylabel("Revenue (USD)")
    frame.ax.set_xlabel("Budget (USD)")
    frame.ax.set_title("Budget vs. Revenue for each Content Rating")

    legend1_line2d = list()
    for step in range(len(rating_color)):
        legend1_line2d.append(mlines.Line2D([0], [0],
                                            linestyle='none',
                                            marker='o',
                                            alpha=0.6,
                                            markersize=6,
                                            markerfacecolor=rating_color[step]))
    frame.ax.legend(legend1_line2d,
                         names,
                         numpoints=1,
                         fontsize=10,
                         loc='lower right',
                         shadow=False)

