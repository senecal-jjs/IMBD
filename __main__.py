from Tkinter import *
import DB_CONNECTION
import Revenue_Prediction
import Popularity


class BuildMenu(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.init_gui()

    def init_gui(self):
        self.master.title("IMBD Data Analysis")
        self.pack(fill=BOTH, expand=1)

        # Button to select revenue prediction
        load_button = Button(self, text="Predict Revenue", command=self.predict_revenue)
        load_button.grid(row=0, column=0)

        # Button to select genre popularity
        load_button = Button(self, text="Genre Popularity", command=self.genre_popularity)
        load_button.grid(row=1, column=0)

        # Button to select user rating prediction
        load_button = Button(self, text="Predict User Rating", command=self.predict_rating)
        load_button.grid(row=2, column=0)

        # Button to select content rating analysis
        load_button = Button(self, text="Content Rating Analysis", command=self.content_rating)
        load_button.grid(row=3, column=0)

        # Button to select runtime analysis
        load_button = Button(self, text="Runtime Analysis", command=self.runtime_analysis)
        load_button.grid(row=4, column=0)

    def predict_revenue(self):
        data = DB_CONNECTION.retrieve_data("predict_revenue")
        Revenue_Prediction.calculate(data)

    def genre_popularity(self):
        data = DB_CONNECTION.retrieve_data("genre_popularity")
        Popularity.calculate(data)

    def predict_rating(self):
        pass

    def content_rating(self):
        pass

    def runtime_analysis(self):
        pass


if __name__ == '__main__':
    root = Tk()
    app = BuildMenu(root)
    root.mainloop()

    # dat = DB_CONNECTION.retrieve_data("runtime_analysis")
    # print(dat.content['PG-13'])