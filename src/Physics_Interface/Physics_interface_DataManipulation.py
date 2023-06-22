
from time import sleep, time
from typing import Tuple, List
import configparser as cp
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


class SaveData(tk.Toplevel):
    """Window to save data to a path and filename"""

    alive = False
    """Boolean to check if the SaveData is alive"""

    def __init__(self, parent):
        """ Initialize the window """
        super().__init__(parent)

        # Titel boven de GUI
        self.title("Data Opslaan")

        # Niet resizable
        self.resizable(False, False)

        self.datax = None
        """X data to be saved"""
        self.datay = None
        """Y data to be saved"""
        self.stdy = None
        """Standard deviation of the y data to be saved"""

        # Global row counter
        self.row = 0

        # Settings aanmaken
        self.label_entry_path = ttk.Label(master=self, text="Path")
        self.label_entry_path.grid(row=self.row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        self.row += 1
        self.Entry_path = ttk.Entry(master=self)
        self.Entry_path.grid(row=self.row, column=0, sticky="NSEW", columnspan=1,
                     rowspan=1)
        self.row += 1

        self.label_entry_filename = ttk.Label(master=self, text="Filename")
        self.label_entry_filename.grid(row=self.row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        self.row += 1

        self.Entry_filename = ttk.Entry(master=self)
        self.Entry_filename.grid(row=self.row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        self.row += 1
        Button_save = ttk.Button(master=self, text="Save", command=self.save_data)
        Button_save.grid(row=self.row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        self.row += 1

        self.__class__.alive = True

    def load_data_from_main(self, datax, datay, stdy):
        """
        Load data from the main window

        :param datax: X data to be saved, from the main window
        :type datax: np.ndarray

        :param datay: Y data to be saved, from the main window
        :type datay: np.ndarray

        :param stdy: Standard deviation of the y data to be saved, from the main window
        :type stdy: np.ndarray

        :return: None
        """
        self.datax = datax
        self.datay = datay
        self.stdy = stdy

    def save_data(self):
        """ Save data to a path and filename, if no path is given, save to ../data """
        path = self.Entry_path.get()
        filename = self.Entry_filename.get()

        if path == "":
            path = "../data"

        data_arr = np.array([self.datax[1:], self.datay[1:], self.stdy[1:]]).T

        np.savetxt(path+"/"+filename+".txt", data_arr)

        notif = Saved_data_notif(self)
        notif.get_path(path, filename)
        notif.message()

    def destroy(self) -> None:
        self.__class__.alive = False
        return super().destroy()

class Saved_data_notif(tk.Toplevel):
    """ Notification window to show the user that the data has been saved """
    def __init__(self, parent):
        """ Initialize the window
        :param parent: Parent window
        :type parent: tk.Toplevel
        """
        super().__init__(parent)

    def get_path(self, path, filename):
        """
        Get the path and filename to be shown in the notification from the SaveData window.

        :param path: Path to the saved file
        :type path: str

        :param filename: Filename of the saved file
        :type filename: str
        """
        self.path = path
        self.filename = filename

    def message(self):
        """ Show the notification """
        self.label = ttk.Label(master=self, text="Data saved to: "+self.path+"/"+self.filename+".txt")
        self.label.grid(row=0, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
