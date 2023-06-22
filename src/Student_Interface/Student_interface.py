import queue
import sys
import threading
import time
import tkinter as tk
import numpy as np
from tkinter import ttk
import configparser as cp

from queue import Queue, Empty
from threading import Thread


try:
    from Physics_Interface.Physics_interface import generate_data, single_data
except ImportError:
    pass

class Student_start_measurement(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Meting starten")

        self.config_path = "../src/cfg_variable.config"

        self.path2ref = None

        self.nrofmeasurementsstudent = None
        """Het aantal meetpunten dat in een meting zit"""

        self.student_measurementtime = None
        """De tijd die het kost om een meting uit te voeren"""

        self.student_measurementtype = None
        """Wordt het resultaat weergeven als transmissie of OD waarde"""

        self.marge = None
        """De marge die wordt gebruikt om te bepalen of de opstelling goed is"""

        self.initialise_config_data()

        self.refdata = np.loadtxt(self.path2ref, dtype=float)
        """De referentie data"""

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
        """
        Laat een progressiebalk zien zolang de meting verloopt en voer een functie uit met het resultaat van de meting.

        :param targfunction: De functie die wordt uitgevoerd om de meting te starten, deze functie wordt uitgevoerd in een thread en moet een queue als argument hebben.
        :type targfunction: callable

        :param label_text: De tekst die wordt weergegeven boven de progressiebalk.
        :type label_text: str

        :param result_function: De functie die wordt uitgevoerd met het resultaat van de meting, deze functie moet een een 2d numpy array als argument hebben.
        :type result_function: callable

        :return: None
        """
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

        self.thread = Thread(target=targfunction, args=(self.queue,))
        self.thread.start()

        self.await_results(self.queue, function=result_function)

    def await_results(self, q: queue.Queue =None, function: callable = None):
        """
        Controleer de queue herhaaldelijk of er al resultaten zijn gerappoteerd. Als er resultaten zijn, voer dan de meegegeven functie uit.
         met deze resultaten en leeg de queue.

        :param q: De queue waar het resultaat in wordt gestopt.
        :type q: Queue
        :param function: De functie die wordt uitgevoerd met het resultaat.
        :type function: function

        :return: None
        """

        try:
            result = q.get(block=False)
        except Empty:
            self.after(100, self.await_results, q, function)
            result = None

        if result is not None:
            function(result)
            with q.mutex:
                q.queue.clear()


    def update_startup(self, verification_succeeded: bool) -> None:
        """
        Update de GUI na het opstarten van de meting. Als het is gelukt, dan wordt er een knop toegevoegd om de meting te starten.
        Als het niet is gelukt, dan wordt er een knop toegevoegd om het opnieuw te proberen.
        :param verification_succeeded: True als het is gelukt, False als het niet is gelukt.
        :type verification_succeeded: bool

        :return: None
        """
        if verification_succeeded:
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

    def verification_measurement(self, q: queue.Queue = None):
        """

        Verifieer of de opstelling goed is. Dit wordt gedaan door de gemiddelde waarde van de referentie data te vergelijken met de gemiddelde waarde van de meting.

        :param q: De queue waar het resultaat (bool) in wordt gestopt.
        :return: None
        """
        data = self.data_source(500, 0)
        data_avg = np.average(data[1])

        marge = self.marge

        print(data_avg, self.refavg)
        if np.all(data_avg > self.refavg - marge) and np.all(data_avg < self.refavg + marge):
            q.put(True)
        else:
            q.put(False)

    def measurement_start(self):
        """Start de meting frame om het herhaalbaar te maken"""
        self.measure_frame(self.measurement, label_text="Meten...",
                           result_function=self.result_analysis)



    def measurement(self, q=None):
        """
        Start de meting in een aparte thread en stop de resultaten in een queue.

        :param q: De queue waar de resultaten in worden gestopt.
        :type q: Queue

        :return: None
        """
        data = self.data_source(int(self.nrofmeasurementsstudent),
                                meastime=float(self.nrofmeasurementsstudent)/(float(self.student_measurementtime) * 1000))

        q.put(data)

    def result_analysis(self, result: np.ndarray):
        """
        Analyseer het resultaat van de meting en geef het resultaat weer

        :param result: De data van de meting uit de queue.
        :type result: np.ndarray

        :return: None
        """
        calculated_result = np.average(result[1])

        if self.student_measurementtype == "0":
            calculated_result = calculated_result/self.refavg * 100
        elif self.student_measurementtype == "1":
            calculated_result = np.log10(self.refavg/calculated_result)

        self.write_to_txt(np.array(result).T)

        self.verification_start.config(text="Resultaat meting: {0:.2f} {1}".format(calculated_result, (lambda: "% wordt doorgelaten." if self.student_measurementtype == "0" else "OD-waarde")()))
        self.progress_bar.stop()
        self.progress_bar.destroy()
        self.frame_row += 1

        self.button_opnieuw = ttk.Button(master=self.frame, text="Opnieuw meten",
                                            command=lambda: self.measure_frame(self.measurement, label_text="Meten...",
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

    def write_to_txt(self, array : np.ndarray):
        """
        Sla de meest recente meting op in een txt bestand met de naam MeestRecenteMeting.txt
        zodat deze altijd op te vragen is door de GUI of voor referentie metingen.

        :param array: op te slaan data, numpy array met 2 kolommen (tijd, voltage)
        :type array: np.ndarray

        :return: None
        """
        np.savetxt("MeestRecenteMeting.txt", array, fmt="%s")

    def stop_measurement(self):
        """
        Zorg ervoor dat alle metingen stoppen en sluit de GUI af.

        :return: None
        """

        self.verification_start.config(text="Opstarten gelukt!")
        self.progress_bar.stop()
        self.progress_bar.destroy()
        self.frame_row += 1

