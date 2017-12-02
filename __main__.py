from Tkinter import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import DB_CONNECTION
import Revenue_Prediction
import Popularity
import Rating_Prediction
import Content_Rating
import Runtime

'''This module contains the functionality for the GUI'''


class BuildMenu(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.master.title("IMBD Data Analysis")
        self.pack(fill=BOTH, expand=1)

        # Button to select revenue prediction
        load_button = Button(self, text="Predict Revenue", command=self.predict_revenue)
        load_button.grid(row=0, column=0)

        # Button to select genre popularity
        load_button = Button(self, text="Genre Popularity", command=self.genre_popularity)
        load_button.grid(row=0, column=1)

        # Button to select user rating prediction
        load_button = Button(self, text="Predict User Rating", command=self.predict_rating)
        load_button.grid(row=0, column=2)

        # Button to select content rating analysis
        load_button = Button(self, text="Content Rating Analysis", command=self.content_rating)
        load_button.grid(row=0, column=3)

        # Button to select runtime analysis
        load_button = Button(self, text="Runtime Analysis", command=self.runtime_analysis)
        load_button.grid(row=0, column=4)

        # Text Box
        self.text = Text(root, height=5, width=30)
        self.text.pack(side=RIGHT, fill=BOTH, expand=1)
        self.text.insert(INSERT, "Hello.....")

        # Embed figure for plots into GUI
        self.f = Figure(figsize=(7, 6), dpi=80)
        self.ax0 = self.f.add_axes((0.1, .1, 1, 1), axisbg=(0.75, 0.75, 0.75), frameon=True)

        self.canvas = FigureCanvasTkAgg(self.f, self.master)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.show()

    # Call the predict revenue analysis
    def predict_revenue(self):
        self.ax0.set_xlabel('Time (s)')
        self.ax0.set_ylabel('Frequency (Hz)')
        self.ax0.plot(np.max(np.random.rand(100, 10) * 10, axis=1), "r-")
        self.canvas.show()
        data = DB_CONNECTION.retrieve_data("predict_revenue")
        Revenue_Prediction.calculate(data)

    # Call the genre popularity analysis
    def genre_popularity(self):
        data = DB_CONNECTION.retrieve_data("genre_popularity")
        Popularity.calculate(data)

    # Call the user rating prediction analysis
    def predict_rating(self):
        data = DB_CONNECTION.retrieve_data("predict_rating")
        Rating_Prediction.calculate(data)

    # Call the content rating analysis
    def content_rating(self):
        data = DB_CONNECTION.retrieve_data("content_rating")
        Content_Rating.calculate(data)

    # Call the runtime analysis
    def runtime_analysis(self):
        data = DB_CONNECTION.retrieve_data("runtime_analysis")
        Runtime.calculate(data)


if __name__ == '__main__':
    root = Tk()
    app = BuildMenu(root)
    root.mainloop()
