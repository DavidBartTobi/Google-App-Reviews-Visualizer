import webbrowser
from tkinter import messagebox
from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
from google_play_scraper import Sort, reviews_all
import matplotlib.pyplot as plt
import gui

class Program:

    def __init__(self, root):

        self.root = root
        self.page = 0
        fontStyle = tkFont.Font(family="Lucida Grande", size=9)

        self.app_id = 'App Name'

        self.app_name_entry = Entry(self.root, justify='center', width=30, font=fontStyle)

        self.choose_button = Button(self.root, text="Search", command=lambda: self.scrape(),
                                       width=21, cursor='hand2', font=fontStyle)

        self.explanation_label = Button(self.root, text="Search the app in Google Appstore and copy the id from the"
                                                           " address bar", font=fontStyle, command=lambda:
        webbrowser.open('https://play.google.com/store',new=1))

        self.example_frame = LabelFrame(self.root)


        #secondary

        self.stats_button = Button(self.root, text='Statistics', command=self.statistics, width=21, cursor='hand2',
                                   font=fontStyle)

        self.reviews_button = Button(self.root, text='Reviews', command=self.review_grid, width=21, cursor='hand2',
                                     font=fontStyle)

        self.return_main_button = Button(self.root, text="❮ Back ", command=self.return_main, width=21, cursor='hand2',
                                         font=fontStyle)

        #reviews

        self.review_frame = LabelFrame(self.root)

        self.review_label = Label(self.review_frame, height=13, width=50, wraplength=300, font=fontStyle)

        self.score_label = Label(self.root)

        self.prev_review_button = Button(self.root, text='<', command= self.prev_review, width=10, cursor='hand2')

        self.next_review_button = Button(self.root, text='>', command= self.next_review, width=10, cursor='hand2')

        self.review_page_entry = Entry(self.root, justify='center', width=5)

        self.review_page_entry.insert(0, 'No.')

        self.find_review_button = Button(self.root, text='Find Review', command= self.find_review, width=12,
                                         cursor='hand2', font=fontStyle)

        self.return_secondary_button = Button(self.root, text="❮ Back ", command=self.return_secondary, width=21,
                                              cursor='hand2', font=fontStyle)

        self.main_grid()


    def scrape(self):

        self.app_id = self.app_name_entry.get()

        try:
            if len(self.app_id) == 0:
                raise TypeError

            us_reviews = reviews_all(
                self.app_id,
                sleep_milliseconds=0,  # defaults to 0
                lang='en',  # defaults to 'en'
                country='us',  # defaults to 'us'
                sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
            )

            df = pd.DataFrame(np.array(us_reviews), columns=['review'])
            self.df = df.join(pd.DataFrame(df.pop('review').tolist()))

            if len(self.df) == 0:
                raise TypeError

            self.hide_main_grid()
            self.secondary_grid()

        except:
            messagebox.showerror("Error", f"The app id provided does not exist.")


    def main_grid(self):
        self.app_name_entry.grid(row=0, column=0, rowspan=3, padx=(80,0), ipady=5.5, pady=(100,0))
        self.choose_button.grid(row=0, column=2, rowspan=3, padx=(0,80), pady=(101,0), ipady=3)
        self.explanation_label.grid(row=3, columnspan=3, ipadx=10, ipady=3)
        self.example_frame.grid(row=4, column=0, rowspan=5, columnspan=3, pady=(0,50))

        self.example_image = Image.open('logos/example.png')
        self.example_image.thumbnail((400, 300))
        self.resized_image = ImageTk.PhotoImage(self.example_image)
        self.img_label = Label(self.example_frame, image=self.resized_image, bg=gui.Main_Theme_Color())
        self.img_label.grid(row=4, column=0, rowspan=5, columnspan=3)

        self.app_name_entry.delete(0, "end")
        self.app_name_entry.insert(0, 'App Id')
        self.app_name_entry.bind("<FocusIn>", self.unbind_app_entry)
        self.root.bind('<Return>', lambda func: self.scrape())

    def hide_main_grid(self):
        self.app_name_entry.grid_forget()
        self.choose_button.grid_forget()
        self.explanation_label.grid_forget()
        self.example_frame.grid_forget()

    def secondary_grid(self):
        self.stats_button.grid(row=0, column=0, rowspan=6, padx=(70,0), pady=(130,0), ipady=3)
        self.reviews_button.grid(row=0, column=2, rowspan=6, padx=(0,70), pady=(130,0), ipady=3)
        self.return_main_button.grid(row=6, column=0, columnspan=3, pady=(0,70), ipady=3)

    def hide_secondary_grid(self):
        self.stats_button.grid_forget()
        self.reviews_button.grid_forget()
        self.return_main_button.grid_forget()

    def review_grid(self):
        self.review_frame.grid(row=0, column=0, rowspan=2, columnspan=3, pady=(30,0))
        self.review_label.grid(row=0, column=0, rowspan=2, columnspan=3)
        self.score_label.grid(row=2, column=0, columnspan=3, pady=(0,40))
        self.prev_review_button.grid(row=3, column=0, padx=(191,0), ipady=3)
        self.next_review_button.grid(row=3, column=2, padx=(0,191), ipady=3)
        self.review_page_entry.grid(row=4, column=0, ipady=5.5, padx=(150,0))
        self.find_review_button.grid(row=4, column=2,columnspan=2, padx=(0,180), ipady=3)
        self.return_secondary_button.grid(row=5, column=0, columnspan=3, ipady=3)

        self.hide_secondary_grid()
        self.load_rating()

        self.review_label.configure(text=self.df.content[self.page])
        self.root.bind('<Return>', lambda func: self.find_review())
        self.review_page_entry.bind("<FocusIn>", self.unbind_review_entry)
        self.root.bind('<Left>', lambda func: self.prev_review())
        self.root.bind('<Right>', lambda func: self.next_review())

    def hide_review_grid(self):
        self.review_frame.grid_forget()
        self.review_label.grid_forget()
        self.prev_review_button.grid_forget()
        self.next_review_button.grid_forget()
        self.review_page_entry.grid_forget()
        self.find_review_button.grid_forget()
        self.return_secondary_button.grid_forget()
        self.score_label.grid_forget()

    def statistics(self):

        ratings = self.df
        ratings = ratings[ratings['score'].between(0, 5)]
        ratings.dropna(subset=['score'], inplace=True)
        ratings = ratings['score'].to_frame()
        ratings = ratings.score.value_counts().reset_index()

        plt.figure(figsize=(9,4))
        plt.pie(ratings.score, autopct='%1.1f%%', labels=ratings['index'])
        plt.legend(labels=ratings['index'], loc='right', fontsize='small', bbox_to_anchor=(1.02, 0.5))
        plt.axis('equal')
        plt.suptitle('App Rating Data')

        plt.annotate(f'Total No. of reviews: {len(self.df)}', xy=(-2.5, 0.2))
        plt.annotate(f'Total No. of replies \nby the developers: {self.df.replyContent.notnull().sum()}', xy=(-2.5, -0.1))

        plt.show()

    def next_review(self):

        if self.page == len(self.df)-1:
            self.page = 0
        else:
            self.page +=1

        self.load_rating()
        self.review_label.configure(text=self.df.content[self.page])

    def prev_review(self):

        if self.page == 0:
            self.page = len(self.df)-1
        else:
            self.page -=1

        self.load_rating()
        self.review_label.configure(text=self.df.content[self.page])

    def find_review(self):

        try:
            self.review_label.configure(text=self.df.content[int(self.review_page_entry.get())])
            self.page = int(self.review_page_entry.get())
            self.load_rating()
            self.review_page_entry.delete(0, "end")


        except:
            messagebox.showerror("Error", f"Please a number in the range 0 - {len(self.df)-1}")
            self.review_page_entry.focus_force()

    def load_rating(self):

        if self.df.score[self.page] == 1:
            self.image = Image.open('logos/Star_rating_1_of_5.png')

        elif self.df.score[self.page] == 2:
            self.image = Image.open('logos/Star_rating_2_of_5.png')

        elif self.df.score[self.page] == 3:
            self.image = Image.open('logos/Star_rating_3_of_5.png')

        elif self.df.score[self.page] == 4:
            self.image = Image.open('logos/Star_rating_4_of_5.png')

        elif self.df.score[self.page] == 5:
            self.image = Image.open('logos/Star_rating_5_of_5.png')

        self.image.thumbnail((80,80))
        self.resized_image = ImageTk.PhotoImage(self.image)
        self.score_label.configure(image=self.resized_image)

    def return_main(self):
        self.main_grid()
        self.hide_secondary_grid()

    def return_secondary(self):
        self.secondary_grid()
        self.hide_review_grid()

    def unbind_app_entry(self, event):
        self.app_name_entry.delete(0, "end")
        self.app_name_entry.unbind("<FocusIn>")
        return None

    def unbind_review_entry(self, event):
        self.review_page_entry.delete(0, "end")
        self.review_page_entry.unbind("<FocusIn>")
        return None
    
