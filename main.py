from tkinter import *
import requests
import json
from dotenv import load_dotenv
from os import environ
import re
import tksheet


class MovieDatabase:

    def __init__(self):

        load_dotenv("./.env")
        self.link = environ.get("TKMDB_LINK", "http://www.omdbapi.com/?")
        self.apikey = environ.get("TKMDB_APIKEY")

        self.window = Tk()
        self.window.title("Movie Database")
        window_width = 520
        window_height = 420
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(self.number_to_string(window_width) + "x" +
                             self.number_to_string(window_height) + "+" +
                             self.number_to_string((screen_width-window_width)/2) + "+" +
                             self.number_to_string((screen_height-window_height)/2))
        self.window.resizable(FALSE, FALSE)

        self.frame = Frame(self.window)
        self.frame.pack()

        self.text_entry = Entry(self.frame, font="Comic 16", width=30)
        self.text_entry.grid(row=0, column=0, padx=10, pady=10)

        self.button_search = Button(self.frame, text="Search", font="Comic 11 bold", command=self.search_film)
        self.button_search.grid(row=0, column=1, padx=10)

        # self.list = Listbox(self.window)
        # self.list.pack(fill=BOTH, expand=TRUE)

        self.frame2 = Frame(self.window)
        self.frame2.pack(expand=TRUE)

        self.list = tksheet.Sheet(self.frame2, data=[[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(3)]
                                                     for r in range(10)])
        self.list.enable_bindings()
        self.list.grid(row=0, column=0, sticky=NSEW)

        self.window.mainloop()

    @staticmethod
    def clear_trailing(number):
        return ('%f' % number).rstrip('0').rstrip('.')

    def number_to_string(self, number):
        return str(self.clear_trailing(number))

    def search_film(self):
        try:
            request = requests.get(self.link + "s=" + self.replace_spaces(self.text_entry.get()) +
                                   "&apikey=" + self.apikey)
            dictionary = json.loads(request.text)
            medias = []
            for media in dictionary["Search"]:
                medias.insert(len(medias), (media["Title"], media["Year"], media["Type"]))
            self.list.set_sheet_data(data=medias)
        except KeyError:
            self.list.set_sheet_data(data=[["Media not Found"]])

    @staticmethod
    def replace_spaces(name):
        # Remove all non-word characters (everything except numbers and letters)
        name = re.sub(r"[^\w\s]", '', name)
        # Replace all runs of whitespace with a single dash
        name = re.sub(r"\s+", '-', name)
        # Return
        return name


MovieDatabase()
