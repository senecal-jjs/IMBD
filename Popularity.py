from sklearn.neighbors.kde import KernelDensity
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
import collections
from Tkinter import *


def calculate(frame, data):
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

    print(sorted(pre_user_rating_stat, key=lambda k: pre_user_rating_stat[k][0]))

    post_user_rating_stat = {}  # User rating statistics during later era
    for key in post_user.keys():
        post_user_rating_stat[key] = stat(np.mean(post_user[key]), np.min(post_user[key]), np.max(post_user[key]),
                                          np.std(post_user[key]), len(post_user[key]))

    print(pre_user_rating_stat)

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

    # Calculate user rating probability distribution for each genre
    user_distributions = {}
    for key in genre_user.keys():
        X = genre_user[key]
        X = np.array(X)
        X = X.reshape(-1, 1)
        x_grid = np.linspace(0, 10, 100)

        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
        log_pdf = kde.score_samples(x_grid[:, np.newaxis])

        user_distributions[key] = np.exp(log_pdf)

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

    # Print summary statistics to screen
    frame.text.insert(INSERT, "User rating statistics, pre 1990:\n")
    for key in pre_user_rating_stat.keys():
        frame.text.insert(END, "\n" + str(key) + ": MEAN:" + str(pre_user_rating_stat[key].mean) + "STDEV: " + str(pre_user_rating_stat[key].stdev) + "\n")

    frame.text.insert(END, "\n\n\n\n\nUser rating statistics, post 1990:\n")
    for key in post_user_rating_stat.keys():
        frame.text.insert(END, "\n" + str(key) + ": MEAN:" + str(post_user_rating_stat[key].mean) + "STDEV: " + str(
                          post_user_rating_stat[key].stdev) + "\n")

    # Organize data into lists
    pre_means = []
    post_means = []
    names = []
    for key in pre_user_rating_stat.keys():
        if key == "Animation" or key == "Western" or key == "War" or key == "Drama" or key == "Mystery":
            pre_means.append(pre_user_rating_stat[key].mean)
            post_means.append(post_user_rating_stat[key].mean)
            names.append(key)

    # Setting the positions and width for the bars
    pos = list(range(len(pre_means)))
    width = 0.25

    # # Plotting the bars
    # fig, ax = plt.subplots(figsize=(10, 5))

    # Create a bar with pre 1990 data, in position pos,
    frame.ax.bar(pos,
            # pre_data,
            pre_means,
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#EE3224',
            # with label the first value in first_name
            label="Pre - 1990")

    # Create a bar with post 1990 data, in position pos + some width buffer,
    frame.ax.bar([p + width for p in pos],
            # using post_data,
            post_means,
            # of width
            width,
            # with alpha 0.5
            alpha=0.5,
            # with color
            color='#F78F1E',
            # with label the second value in first_name
            label="Post - 1990")

    # Set the y axis label
    frame.ax.set_ylabel('User Rating')

    # Set the chart's title
    frame.ax.set_title('Pre and Post 1990 User Ratings')

    # Set the position of the x ticks
    frame.ax.set_xticks([p + 1.5 * width for p in pos])

    # Set the labels for the x ticks
    frame.ax.set_xticklabels(names)
    frame.ax.set_ylim([0, 10])

    # Make legend
    handles, labels = frame.ax.get_legend_handles_labels()
    frame.ax.legend(handles, labels, loc="upper left")

    # Save figure
    frame.f.savefig("Plots/pre_post_1990_genre_user_rating")
    frame.ax.cla()

    # Send plot of top user rating genre probability distributions to GUI
    x_grid = np.linspace(0, 10, 100)
    frame.ax.plot(x_grid, user_distributions['Animation'], label="Animation")
    frame.ax.plot(x_grid, user_distributions['Western'], label="Western")
    frame.ax.plot(x_grid, user_distributions['War'], label="War")
    frame.ax.plot(x_grid, user_distributions['Drama'], label="Drama")
    frame.ax.set_title("Probability Dist. for Top User Rated Genres")
    frame.ax.set_xlabel('User Rating')
    frame.ax.set_ylabel('Probability')

    handles, labels = frame.ax.get_legend_handles_labels()
    frame.ax.legend(handles, labels, loc="upper left")


