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

# Import the various windows
from src.Physics_Interface.Physics_interface_Settings import Settings
from src.Physics_Interface.Physics_interface_DataManipulation import LoadData, SaveData

global number_of_samples
try:
    from src.Hardware import ADCReader
    adc_reader = ADCReader()
    # Hier iets wat voor nu data genereert om aan te leveren aan Base_interface
    # Dit is een test functie
    def generate_data(samples, tref) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genereer data voor de GUI

        :return: tijd, data
        """
        global adc_reader
        # Maak een array aan van data over de tijd, sleep is om te simuleren dat het even duurt
        nmeasurements = samples  # n nr of meas
        meastime = 0.01  # t per meas

        tstart = tref

        data_arr = np.zeros([nmeasurements, 3])
        for i in range(nmeasurements):
            d, t, s = adc_reader.get_meas(1, meastime, start_time=tstart)
            data_arr[i] = np.array([d, t, s])
        # Return tijd, data
        return data_arr[:, 1], data_arr[:, 0]

    def single_sample():
        global adc_reader
        return adc_reader.read_adc()

except Exception as e:
    print(e)

    def generate_data(samples, tref) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genereer data voor de GUI
        :return: tijd, data
        """
        # Maak een array aan van data over de tijd, sleep is om te simuleren dat het even duurt

        nmeasurements = samples  # n nr of meas
        meastime = 0.01  # t per meas

        data_arr = np.zeros([nmeasurements, 3])

        print(nmeasurements)

        for i in range(nmeasurements):
            d, t, s = np.random.randint(0, 100), meastime*(i+1) + tref, np.random.randint(0, 100)
            data_arr[i] = np.array([d, t, s])
        print(data_arr)
        return data_arr[:, 1], data_arr[:, 0]

    def single_data(tref):
        meastime = 0.01
        return np.array([meastime+tref, np.random.randint(0, 100)], dtype=float)



class Base_physics(tk.Tk):
    def __init__(self):
        super().__init__()

        # Config path
        self.config_path = "../src/cfg_variable.config"

        # Titel boven de GUI
        self.title("Technisch interface")

        # Grootte van de GUI in px
        self.geom = (900, 600)
        self.geometry("%sx%s" % self.geom)

        # Niet resizable
        self.resizable(False, False)

        # Global row counter
        self.row = 0
        self.rowfig = 0

        self.time_start = time()
        self.tref = 0

        ## Vars
        # Algemeen
        self.measurementtype = None
        self.nrofmeasurements = None

        # Grafiek
        self.msperframe = None
        self.xastype = None
        self.yastype = None
        self.stepsize = None

        # RTdata
        self.msperdata = None

        # Vaste parameters
        self.adc2v = None
        self.std = None
        self.path2ref = None

        # Initialise base data arrays
        shape = 100
        self.xaxis = self.data_time = np.zeros(1)
        self.yaxis = self.data_voltage = np.zeros(1)
        print(self.xaxis)
        self.data_time[-1] = self.tref

        # Read the config and update the vars
        self.initialise_config_data()

        # Load and read reference data
        # "../data/reference.txt"
        self.refdata = np.loadtxt(self.path2ref, dtype=float)
        self.refavg = np.average(self.refdata[:, 0])
        self.refstd = np.std(self.refdata[:, 0])
        
        # Settings link
        self.settings_link = Settings
        self.settings_open = None

        ## Build GUI
        # Figsize
        self.dpi = 100
        self.figsize = (
        self.geom[0] / (2 * self.dpi), self.geom[1] / (self.dpi))

        self.Build_GUI_physics()

    def Build_GUI_physics(self):

        self.graph_topleft()

        # Build the right side of the GUI
        avg = str(np.average(self.data_voltage))
        
        # Updated real time data
        self.var_labels = [[str(self.data_voltage[-1]), str(np.average(self.data_voltage)), "2", "3"], ["0", "1", "2", "3"]]
        upd, vals = self.data_box(
            [["Voltage", "Gemmidelde waarde", "Resultaat"],
             ["UV-index", "Transmissie", "OD-waarde"]],
            [[str(self.data_voltage[-1]), avg, 1, "3"], ["0", "1", "2", "3"]],
            "Real time ingelezen data",
            updated=True)

        self.vals = vals
        self.upd = upd[2:]

        # Not changing data
        self.data_box([["Label 1", "Label 11", "label12", "label13"],
                       ["Label 2", "label 21", "label 22", "label 23"]],
                      [["0", "1", "2", "3"], ["0", "1", "2", "3"]],
                      "Resultaten studentmeting")

        # Buttons
        self.data_box([["Reset data", "Meting verichten", "Meting stoppen"],
                       ["Data opslaan", "Meet instellingen aanpassen",
                        "Student meting starten"]],
                      [["Laad", "Start", "Stop"],
                       ["Opslaan", "Instellingen", "Start"]],
                      "Hieronder staan enkele knoppen voor data verwerking.",
                      buttons=True,
                      commands=[
                          [self.reset_data, self.start_meas, self.pause_meas],
                          [self.save_data, self.start_settings, self.pause_meas]])

        self.job = self.update_vars(
            [str(np.random.randint(10)) for i in range(6)])

        return None

    # Configuratie methods
    def initialise_config_data(self) -> None:
        """
        Initialiseer de data uit de config file
        en koppel deze aan de juiste attributen.

        :return: None
        """
        config = cp.ConfigParser()
        config.read(self.config_path)
        self.measurementtype = config["Algemeen"]["typemeting"]
        self.nrofmeasurements = config["Algemeen"]["nmetingen"]

        self.msperframe = config["Grafiek"]["MsPerFrame"]
        self.xastype = config["Grafiek"]["Grafiektypex"]
        self.yastype = config["Grafiek"]["Grafiektypey"]

        self.stepsize = config["Grafiek"]["Stapsgrootte"]

        self.msperdata = config["RTData"]["MsPerData"]

        self.adc2v = config["VasteParameters"]["ADC2V"]
        self.std = config["VasteParameters"]["std"]
        self.path2ref = config["VasteParameters"]["path_to_ref"]

    def update_config_data(self):
        """
        Update de data in de config file, en update gelijk de attributen
        met nieuwe waarden geselecteerd door de gebruiker in de settings window.

        :return: None
        """
        pass

    # Frames en opbouw van de GUI
    def graph_topleft(self):
        """
        Graph in the top left corner
        """

        # Maak een figuur aan
        self.fig = plt.Figure(figsize=self.figsize, dpi=100)
        # self.fig.suptitle("Test")

        # x-labels
        x_labels = ["Tijd $t$ [s]", "Metingen $n$ [-]"]
        y_labels = ["Voltage $V$ [V]", "Intensiteit $I$ [mW/cm$^2$]", "Transmissie $T$ [-]", "Optische dichtheid $OD$ [-]"]

        # Maak een subplot aan
        self.ax = self.fig.add_subplot(111)

        # Maak een plot aan
        self.line, = self.ax.plot(self.xaxis, self.yaxis, linestyle="-", marker="o")

        self.ax.set_xlabel(x_labels[int(self.xastype)])
        self.ax.set_ylabel(y_labels[int(self.yastype)])

        # Maak een canvas aan
        canvas = FigureCanvasTkAgg(self.fig, master=self)

        # Plaats de canvas in de GUI
        self.rowfig = 0
        canvas.get_tk_widget().grid(row=self.rowfig, column=0, sticky="NSEW",
                                    padx=10, pady=10,
                                    columnspan=3, rowspan=6)

        self.ani = animation.FuncAnimation(self.fig, self.animate,
                                           np.arange(0, 100), interval=25,
                                           blit=False)

        # self.after(1000, self.update, generate_data())
        return None

    def animate(self, i):
        self.line.set_xdata(self.xaxis)
        self.line.set_ydata(self.yaxis)

        self.ax.set_xlim(min(self.xaxis), max(self.xaxis))
        self.ax.set_ylim(min(self.yaxis), max(self.yaxis))
        return self.line,

    def data_box(self, txt_labels: List[List[str]],
                 entries: List[List[str or float]], explain_text: str,
                 buttons: bool = False,
                 edit_state: bool = False, commands: List = None,
                 updated: bool = False) -> List[tk.Entry] or None:
        """
        Data box with 2x3 data cells where each cell has a label and an entry
        :param txt_labels: List of labels [[row], [row]]
        :param entries: List of entries [[row], [row]]
        :param buttons: True, entries become buttons
        :param edit_state: True if the entries need to be editable
        :param commands: List of commands for the buttons
        :return: List of entries or buttons if edit_state or buttons is True
        """
        # Maak een label aan
        text_src = explain_text
        label = tk.Label(master=self, text=text_src)
        label.grid(row=self.row, column=4, sticky="NSEW", columnspan=3,
                   rowspan=1)
        self.row += 1

        if edit_state:
            entries = []
        variables = []

        # Hier komt de frame met alle data
        frame_data = tk.Frame(master=self)

        entrnr = 0
        labelnr = 0

        # Loop door alle lables en entries heen (row, column)
        for i in range(4):
            for j in range(3):
                if i % 2 == 0:
                    # Maak een label aan
                    try:
                        label = tk.Label(master=frame_data,
                                         text=txt_labels[labelnr][j])
                    except IndexError:
                        label = tk.Label(master=frame_data, text="")
                    # Plaats de label in het frame
                    label.grid(row=i, column=j, sticky="NSEW")
                else:
                    if buttons:
                        try:
                            button = tk.Button(master=frame_data,
                                               text=entries[entrnr][j],
                                               command=commands[entrnr][j])
                        except IndexError:
                            button = tk.Button(master=frame_data, text="",
                                               command=lambda x=0: None)
                        button.grid(row=i, column=j, sticky="NESW")
                        entries.append(button)
                    else:
                        try:
                            strvar = tk.StringVar(
                                value=str(entries[entrnr][j]))
                            # strvar.trace("w", self.update_plc)
                        except IndexError:
                            strvar = tk.StringVar(value="")
                            # strvar.trace("w", self.update_plc)

                        # Maak een entry aan
                        entry = tk.Entry(master=frame_data,
                                         textvariable=strvar)
                        entry.setvar(str(strvar), str(entries[entrnr][j]))
                        entry.config(
                            state="readonly" if not edit_state else "normal")
                        # Plaats de entry in het frame
                        entry.grid(row=i, column=j, sticky="NSEW")

                        if edit_state or buttons or updated:
                            entries.append(entry)
                            variables.append(strvar)

            if i % 2 == 0:
                labelnr += 1
            else:
                entrnr += 1

        frame_data.grid(row=self.row, column=4, sticky="NSEW", columnspan=1,
                        rowspan=1)
        self.row += 1

        return (entries, variables) if (
                    edit_state or buttons or updated) else None

    # Data acquisitie methodes
    def read_ndatapoints(self) -> List[str]:
        """
        Lees n punten uit en ververs de bestaande array (meting=1)
        :param args:
        :return:
        """
        avg, std = np.average(self.data_voltage), np.std(self.data_voltage)
        transmissie = avg/self.refavg

        return ["{:>5.6f}".format(self.data_voltage[-1]),
                "{:>5.6f} ± {:>5.4f}".format(avg, std),
                "{:>5.6f}".format(self.calculate_intesnity(avg)),
                str(0), transmissie, np.log10(1/transmissie)]

    # Real time data verwerking en after methode
    def update_vars(self, *args) -> str:
        """
        Update the variables in the GUI

        :param args[0]: Function that generates the data
        :param args[1]: Data points for all 6 boxes

        :return: None
        """
        if len(args) == 1:
            args = [args[0]]
        # self.graph_topleft(args[0]())
        for en in range(len(self.vals)):
            self.vals[en].set(args[0][en])
            self.upd[en].config(state="normal")
            self.upd[en].setvar(str(self.vals[en]), str(self.vals[en].get()))
            self.upd[en].config(state="readonly")

        # self.animate(1)

        if self.measurementtype == str(0):
            self.data_time, self.data_voltage = generate_data(int(self.nrofmeasurements), tref=self.data_time[-1])
        else:
            data = single_data(self.data_time[-1])

            self.data_time = np.append(self.data_time, data[0])
            self.data_voltage = np.append(self.data_voltage, data[1])

        if self.xastype == str(0):
            data_time = self.data_time
        elif self.xastype == str(1):
            data_time = list(range(len(self.data_time)))

        if self.yastype == str(0):
            data_voltage = self.data_voltage
        elif self.yastype == str(1):
            data_voltage = self.calculate_intesnity(self.data_voltage)
        elif self.yastype == str(2):
            data_voltage = self.calculate_intesnity(self.data_voltage)/self.refavg
        elif self.yastype == str(3):
            data_voltage = np.log10(np.abs(self.refavg/self.calculate_intesnity(self.data_voltage)))

        self.xaxis = data_time
        self.yaxis = data_voltage

        print(self.call("after", "info"))

        job = self.after(1000, self.update_vars,
                         self.read_ndatapoints())  # 1000ms = 1s

        return job

    # Gelinkte functies

    def calculate_intesnity(self, x):
        # https://learn.sparkfun.com/tutorials/ml8511-uv-sensor-hookup-guide/all
        # Linear equation between 0 and 15mW/cm^2 and 1 and 3 V output
        return (x-0.99) * 15/2 + 1

    def reset_data(self):

        self.pause_meas()

        self.xaxis = self.data_time = np.zeros(1)
        self.yaxis = self.data_voltage = np.zeros(1)

        self.start_meas()

        return None

    def save_data(self):
        if not SaveData.alive:
            sv = SaveData(self)
            sv.load_data_from_main(self.data_time, self.data_voltage, self.calculate_intesnity(self.data_voltage))
        return "data saved"

    def pause_meas(self):
        """
        Stop the update_vars job and set self.job to None

        :return: None
        """
        # Stop de meting, als er een meting loopt
        if self.job is not None:
            # Zoek de exacte job en stop deze met after_cancel
            jobs = self.call("after", "info")
            for i in jobs:
                self.after_cancel(i)

            # De meting is gestopt dus job is None
            self.job = None
        return None

    def start_meas(self):
        """
        Restart the update_vars job and set self.job to the job

        :return: None
        """
        # Check of er al een meting loopt
        if self.job is None:
            self.graph_topleft()
            self.job = self.update_vars(self.read_ndatapoints())

        return None

    def start_settings(self):
        """
        Start the settings window

        :return: None
        """
        # Check of er al een settings window open is
        if not Settings.alive:
            self.settings_open = Settings(self)


        return None

    def start_student_measurement(self):
        self.pause_meas()


    def destroy(self) -> None:
        self.pause_meas()
        self.fig.clear()
        return super().destroy()




