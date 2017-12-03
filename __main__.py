from Tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
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

        # Text Box to display summary of analysis
        self.text = Text(root, height=5, width=60)
        self.text.pack(side=RIGHT, fill=BOTH, expand=1)

        # Embed figure for plots into GUI
        self.f = plt.figure(1)
        self.ax = self.f.add_subplot(111)
        plt.ion()

        self.canvas = FigureCanvasTkAgg(self.f, self.master)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.show()

    # Call the predict revenue analysis
    def predict_revenue(self):
        self.text.delete(1.0, END)
        self.ax.cla()
        data = DB_CONNECTION.retrieve_data("predict_revenue")
        Revenue_Prediction.calculate(self, data)
        self.f.canvas.draw()
        self.f.savefig("Plots/_revenue_dist")

    # Call the genre popularity analysis
    def genre_popularity(self):
        self.text.delete(1.0, END)
        self.ax.cla()
        data = DB_CONNECTION.retrieve_data("genre_popularity")
        Popularity.calculate(self, data)
        self.f.canvas.draw()
        self.f.savefig("Plots/user_rating_genre_dist")

    # Call the user rating prediction analysis
    def predict_rating(self):
        self.text.delete(1.0, END)
        self.ax.cla()
        data = DB_CONNECTION.retrieve_data("predict_rating")
        Rating_Prediction.calculate(self, data)
        self.f.canvas.draw()
        self.f.savefig("Plots/user_rating_prediction")

    # Call the content rating analysis
    def content_rating(self):
        self.text.delete(1.0, END)
        self.ax.cla()
        data = DB_CONNECTION.retrieve_data("content_rating")
        Content_Rating.calculate(self, data)
        self.f.canvas.draw()
        self.f.savefig("Plots/bubble")

    # Call the runtime analysis
    def runtime_analysis(self):
        self.text.delete(1.0, END)
        self.ax.cla()
        data = DB_CONNECTION.retrieve_data("runtime_analysis")
        Runtime.calculate(self, data)
        self.f.canvas.draw()
        self.f.savefig("Plots/content_rating_runtime_dist")


if __name__ == '__main__':
    root = Tk()
    app = BuildMenu(root)
    root.mainloop()
