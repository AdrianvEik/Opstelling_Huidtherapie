import threading
import time
import tkinter as tk
import numpy as np
from tkinter import ttk
import configparser as cp

from queue import Queue, Empty
from threading import Thread

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
        self.marge = None

        self.initialise_config_data()

        self.refdata = np.loadtxt(self.path2ref, dtype=float)
        self.refavg = np.average(self.refdata[:, 0])
        self.refstd = np.std(self.refdata[:, 0])

        # Grootte van de GUI in px
        self.geom = (900, 600)
        self.geometry("%sx%s" % self.geom)

        self.resizable(False, False)

        # Global row counter
        self.row = 0

        self.data_source = None
        self.data_source_single = None

        self.queue = Queue()

        self.frame = tk.Frame(master=self)


    def measure_frame(self, targfunction, label_text="Opstarten...", result_function=None):
        """Display a frame wih a progress bar while a thread is running"""
        for child in self.frame.winfo_children():
            child.destroy()

        self.frame_row = 0

        self.verification_start = tk.Label(master=self.frame, text=label_text)
        self.verification_start.grid(row=self.frame_row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        self.frame_row += 1

        self.progress_bar = ttk.Progressbar(master=self.frame, orient="horizontal", length=200,
                                       mode="indeterminate", maximum=70)
        self.progress_bar.grid(row=self.frame_row, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
        self.progress_bar.start()

        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        threading.Thread(target=targfunction, args=(self.queue,)).start()

        self.await_results(self.queue, function=result_function)

    def await_results(self, queue=None, function=None):
        try:
            result = queue.get(block=False)
        except Empty:
            self.after(100, self.await_results, queue, function)
            result = None
        print(result)
        if result is not None:
            function(result)
            with queue.mutex:
                queue.queue.clear()


    def update_startup(self, bool) -> None:

        if bool:
            self.verification_start.config(text="Opstarten gelukt!")
            self.progress_bar.stop()
            self.progress_bar.destroy()
            self.frame_row += 1
            Button_start = ttk.Button(master=self.frame, text="Start meting",
                                      command=self.measurement_start)
            Button_start.grid(row=self.frame_row, column=0, sticky="NSEW",
                              columnspan=1,
                              rowspan=1)

        else:
            self.verification_start.config(text="Opstarten mislukt!")
            self.progress_bar.stop()
            self.progress_bar.destroy()
            self.frame_row += 1
            Button_start = ttk.Button(master=self.frame, text="Opnieuw starten",
                                      command=lambda: self.measure_frame(self.verification_measurement,
                                                                        result_function=self.update_startup))
            Button_start.grid(row=self.frame_row, column=0, sticky="NSEW",
                              columnspan=1,
                              rowspan=1)
            # Toch doorgaan met meten?
            Button_doorgaan = ttk.Button(master=self.frame, text="Toch meten?",
                                         command=self.measurement_start)
            Button_doorgaan.grid(row=self.frame_row, column=1, sticky="NSEW",
                                 columnspan=1,
                                 rowspan=1)

    def verification_measurement(self, queue=None):
        """Verify if the setup is working, return True if it is"""
        data = self.data_source(500, 0)
        data_avg = np.average(data[1])

        marge = self.marge

        print(data_avg, self.refavg)
        if np.all(data_avg > self.refavg - marge) and np.all(data_avg < self.refavg + marge):
            queue.put(True)
        else:
            queue.put(False)

    def measurement_start(self):
        self.measure_frame(self.measurement, label_text="Meten...",
                           result_function=self.result_analysis)

    def measurement(self, queue=None):
        """Start a measurement"""
        data = self.data_source(int(self.nrofmeasurementsstudent), time.time(),
                                meastime=float(self.student_measurementtime))

        queue.put(data)

    def result_analysis(self, result):

        calculated_result = np.average(result[1])

        self.verification_start.config(text="Resultaat meting: {0}".format(calculated_result))
        self.progress_bar.stop()
        self.progress_bar.destroy()
        self.frame_row += 1

        self.button_opnieuw = ttk.Button(master=self.frame, text="Opnieuw meten",
                                            command=lambda: self.measure_frame(self.measurement,
                                                                                result_function=self.result_analysis))
        self.button_opnieuw.grid(row=self.frame_row, column=0, sticky="NSEW",
                                    columnspan=1,
                                    rowspan=1)



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
        self.marge = float(config["StudentMeting"]["marge_student_verify"])
