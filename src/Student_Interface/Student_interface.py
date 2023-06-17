
import tkinter as tk
import numpy as np
from tkinter import ttk
import configparser as cp

try:
    from src.Physics_Interface.Physics_interface import generate_data, single_data
except ImportError:
    pass

# parent = tk.Tk() if __name__ == "__main__" else tk.Toplevel()
class Student_start_measurement(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Meting starten")

        self.config_path = "../src/cfg_variable.config"

        self.path2ref = None

        self.nrofmeasurementsstudent = None
        self.student_measurementtime = None
        self.student_measurementtype = None

        self.initialise_config_data()

        # Grootte van de GUI in px
        self.geom = (900, 600)
        self.geometry("%sx%s" % self.geom)

        self.resizable(False, False)

        # Global row counter
        self.row = 0

        self.data_source = None
        self.data_source_single = None
        self.verify_frame()

    def verify_frame(self):
        """Verify if all settings are correct"""
        frame = tk.Frame(master=self)
        frame_row = 0

        verification_start = tk.Label(master=frame, text="Opstarten...")
        verification_start.grid(row=frame_row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        frame_row += 1

        progress_bar = ttk.Progressbar(master=frame, orient="horizontal", length=200,
                                       mode="indeterminate", maximum=70)
        progress_bar.grid(row=frame_row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        progress_bar.start()

        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def start_meting_frame(self):
        """Frame to start a measurement"""
        pass


    def initialise_config_data(self) -> None:
        """
        Initialiseer de data uit de config file
        en koppel deze aan de juiste attributen.

        :return: None
        """
        config = cp.ConfigParser()
        config.read(self.config_path)
        self.path2ref = config["VasteParameters"]["path_to_ref"]

        self.nrofmeasurementsstudent = config["StudentMeting"]["measurement"]
        self.student_measurementtime = config["StudentMeting"]["measurement_time"]
        self.student_measurementtype = config["StudentMeting"]["measurement_type"]