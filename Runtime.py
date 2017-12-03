from sklearn.neighbors.kde import KernelDensity
import numpy as np
import collections
from operator import itemgetter
from Tkinter import *

'''Print the summary statistics in rating_runtime_stat and genre_runtime_stat'''


def calculate(frame, data):
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

        genre_runtime_dist[key] = np.exp(log_pdf)

    # Calculate runtime probability distribution for each rating
    rating_runtime_dist = {}
    for key in data.content.keys():
        X = data.content[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 200, 200)

        kde = KernelDensity(kernel='gaussian', bandwidth=10).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        rating_runtime_dist[key] = np.exp(log_pdf)

    # Print summary statistics to screen
    frame.text.insert(INSERT, "Content Rating Runtime Stats:\n")
    for key in rating_runtime_stat.keys():
        frame.text.insert(END, "\n" + str(key) + ": MEAN:" + str(rating_runtime_stat[key].mean) + " STDEV: " + str(
            rating_runtime_stat[key].stdev) + "\n")

    frame.text.insert(END, "\n\n\n\n\nGenre Runtime Stats:\n")
    for key in genre_runtime_stat.keys():
        frame.text.insert(END, "\n" + str(key) + ": MEAN:" + str(genre_runtime_stat[key].mean) + " STDEV: " + str(
                          genre_runtime_stat[key].stdev) + "\n")

    # Save bar charts of mean runtime
    rating_means_names = []

    for key in rating_runtime_stat.keys():
        if key == "G" or key == "PG" or key == "PG-13" or key == "R":
            rating_means_names.append((rating_runtime_stat[key].mean, key))

    temp = sorted(rating_means_names, key=itemgetter(1))
    a = temp[2]
    temp[2] = temp[3]
    temp[3] = a

    rating_means = []
    rating_names = []

    for pt in temp:
        rating_means.append(pt[0])
        rating_names.append(pt[1])

    ind = np.arange(len(rating_means))
    frame.ax.set_ylabel('Runtime (min)')
    frame.ax.set_title('Runtime by Content Rating')
    frame.ax.set_xticks([p + 0.2 for p in ind])
    frame.ax.set_xticklabels(rating_names)
    frame.ax.bar(ind, rating_means, width=0.5)
    frame.f.savefig("Plots/bar_rating_runtime")
    frame.ax.cla()

    # Send figure to GUI
    x_grid = np.linspace(0, 200, 200)
    frame.ax.plot(x_grid, rating_runtime_dist['G'], label="G")
    frame.ax.plot(x_grid, rating_runtime_dist['PG'], label="PG")
    frame.ax.plot(x_grid, rating_runtime_dist['PG-13'], label="PG-13")
    frame.ax.plot(x_grid, rating_runtime_dist['R'], label="R")
    frame.ax.set_title("Probability Dist. for Common Ratings")
    frame.ax.set_xlabel('Runtime')
    frame.ax.set_ylabel('Probability')

    handles, labels = frame.ax.get_legend_handles_labels()
    frame.ax.legend(handles, labels)