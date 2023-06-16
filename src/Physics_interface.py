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

try:
    from Hardware import ADCReader
    adc_reader = ADCReader()
    # Hier iets wat voor nu data genereert om aan te leveren aan Base_interface
    # Dit is een test functie
    def generate_data() -> Tuple[np.ndarray, np.ndarray]:
        """
        Genereer data voor de GUI

        :return: tijd, data
        """
        global adc_reader
        # Maak een array aan van data over de tijd, sleep is om te simuleren dat het even duurt
        nmeasurements = 100  # n nr of meas
        meastime = 0.01  # t per meas

        tstart = time()

        data_arr = np.zeros([nmeasurements, 3])
        for i in range(nmeasurements):
            d, t, s = adc_reader.get_meas(1, meastime, start_time=tstart)
            data_arr[i] = np.array([d, t, s])
        # Return tijd, data
        return data_arr[:, 1], data_arr[:, 0]
except Exception as e:
    print(e)

    def generate_data() -> Tuple[np.ndarray, np.ndarray]:
        """
        Genereer data voor de GUI
        :return: tijd, data
        """
        # Maak een array aan van data over de tijd, sleep is om te simuleren dat het even duurt
        data = np.random.rand(100)
        # Return tijd, data
        return np.linspace(0, 1, 100), data



class Base_physics(tk.Tk):
    def __init__(self):
        super().__init__()
        # Config path
        self.config_path = os.path.join(os.path.dirname(__file__),
                                        "cfg.config")

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

        # Initialise base data arrays
        shape = 100
        self.data_time = np.zeros(shape)
        self.data_voltage = np.zeros(shape)

        # Read the config and update the vars
        self.initialise_config_data()

        # Settings link
        self.settings_link = Settings
        self.settings_open = None

        # Data acquisititie methode
        # Afhankelijk van de instellingen in de config file wordt dit aangepast
        if self.measurementtype == None:
            self.acquisition_method = generate_data  # returns time, data (np.ndarray)
        elif self.measurementtype == "0":
            self.acquisition_method = generate_data  # returns time, data (np.ndarray)
        elif self.measurementtype == "1":
            self.acquisition_method = generate_data  # returns time, data (np.ndarray)

        ## Build GUI
        # Figsize
        self.dpi = 100
        self.figsize = (
        self.geom[0] / (2 * self.dpi), self.geom[1] / (self.dpi))

        self.Build_GUI_physics()

    def Build_GUI_physics(self):

        self.graph_topleft()

        # Build the right side of the GUI

        # Updated real time data
        self.var_labels = [[str(self.data_voltage[-1]), str(np.average(self.data_voltage)), "2", "3"], ["0", "1", "2", "3"]]
        upd, vals = self.data_box(
            [["Voltage", "Gemmidelde waarde", "Resultaat"],
             ["Label 2", "label 21", "label 22", "label 23"]],
            [[str(self.data_voltage[-1]), str(np.average(self.data_voltage)), "2", "3"], ["0", "1", "2", "3"]],
            "Real time ingelezen data",
            updated=True)

        self.vals = vals
        self.upd = upd[2:]

        # Not changing data
        self.data_box([["Label 1", "Label 11", "label12", "label13"],
                       ["Label 2", "label 21", "label 22", "label 23"]],
                      [["0", "1", "2", "3"], ["0", "1", "2", "3"]],
                      "Meest recent ingelezen data")

        # Buttons
        self.data_box([["Data inladen", "Meting verichten", "Meting stoppen"],
                       ["Data opslaan", "Meet instellingen aanpassen",
                        "Grafiek opslaan"]],
                      [["Laad", "Start", "Stop"],
                       ["Opslaan", "Instellingen", "Opslaan"]],
                      "Hieronder staan enkele knoppen voor data verwerking.",
                      buttons=True,
                      commands=[
                          [self.load_data, self.start_meas, self.pause_meas],
                          [self.save_data, self.start_settings, self.results]])

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
        self.fig.suptitle("Test")

        # Maak een subplot aan
        self.ax = self.fig.add_subplot(111)
        # Maak een plot aan
        self.line, = self.ax.plot(self.data_time, self.data_voltage)
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
        self.line.set_xdata(self.data_time)
        self.line.set_ydata(self.data_voltage)

        self.ax.set_xlim(min(self.data_time), max(self.data_time))
        self.ax.set_ylim(min(self.data_voltage), max(self.data_voltage))
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
    def read_realtime_data(self, *args) -> str:
        """
        Lees enkele punten uit en voeg toe aan de bestaande array (meting=0)
        :param args:
        :return:
        """
        return str(np.random.randint(10))

    def read_ndatapoints(self, *args) -> List[str]:
        """
        Lees n punten uit en ververs de bestaande array (meting=1)
        :param args:
        :return:
        """
        avg, std = np.average(self.data_voltage), np.std(self.data_voltage)

        return ["{:>5.6f}".format(self.data_voltage[-1]),
                "{:>5.6f} ± {:>5.4f}".format(avg, std),
                "{:>5.6f}".format(self.calculate_intesnity(avg)),
                str(0), str(1), str(2)]

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
        print(args)
        # self.graph_topleft(args[0]())
        for en in range(len(self.vals)):
            self.vals[en].set(args[0][en])
            self.upd[en].config(state="normal")
            self.upd[en].setvar(str(self.vals[en]), str(self.vals[en].get()))
            self.upd[en].config(state="readonly")

        # self.animate(1)

        data_time, data_voltage = generate_data()
        self.data_voltage = data_voltage
        self.data_time = data_time

        job = self.after(1000, self.update_vars,
                         self.read_ndatapoints())  # 1000ms = 1s

        return job

    # Gelinkte functies
    def get_data(self):
        # This function should be called to request data from the hardware.py file
        # And format it to be used in the graph/real time data

        # This is a placeholder

        # Wellicht functie als dit in hardware.py?
        # return should contain (tijd, data, avg, hardware informatie [voltage, laatst gelezen waarde, int value, etc.])
        return None

    def calculate_intesnity(self, x):
        # https://learn.sparkfun.com/tutorials/ml8511-uv-sensor-hookup-guide/all
        # Linear equation between 0 and 15mW/cm^2 and 1 and 3 V output
        return (x-0.99) * 2 / 15 + 1

    def load_data(self):
        print("ld")
        return "data loaded"

    def save_data(self):
        print("sv")
        if not SaveData.alive:
            sv = SaveData(self)
            sv.load_data_from_main(self.data_time, self.data_voltage, self.calculate_intesnity(self.data_voltage))
        return "data saved"

    def results(self):
        print("rs")
        return "results"

    def pause_meas(self):
        """
        Stop the update_vars job and set self.job to None

        :return: None
        """
        # Stop de meting, als er een meting loopt
        print(self.job)
        print(self.call("after", "info"))
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
            self.job = self.update_vars(
                [str(np.random.randint(10)) for i in range(6)])

        return None

    def start_settings(self):
        """
        Start the settings window

        :return: None
        """
        # Check of er al een settings window open is
        if self.settings_open is None:
            self.settings_open = Settings()

        return None


class Settings(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

        # Titel boven de GUI
        self.title("Instellingen")

        # Grootte van de GUI in px
        self.geom = (900, 600)
        self.geometry("%sx%s" % self.geom)

        # Niet resizable
        self.resizable(False, False)

        # Global row counter
        self.row = 0

        # Settings aanmaken
        self.build_settings()

    def build_settings(self):
        frame = tk.Frame(master=self)
        framerow = 0
        # Maak een label aan
        label = tk.Label(master=frame, text="Settings")
        label.grid(row=framerow, column=0, sticky="NSEW", columnspan=1,
                   rowspan=1)
        entry = tk.Entry(master=frame)
        entry.grid(row=framerow, column=1, sticky="NSEW", columnspan=1,
                   rowspan=1)
        framerow += 1

        frame.grid(row=self.row, column=0, sticky="NSEW", columnspan=1,
                   rowspan=1)
        self.row += 1


class LoadData(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

class SaveData(tk.Toplevel):
    "Window to save data to a path and filename"

    alive = False
    def __init__(self, parent):
        super().__init__(parent)

        # Titel boven de GUI
        self.title("Data Opslaan")

        # Grootte van de GUI in px
        self.geom = (400, 400)
        self.geometry("%sx%s" % self.geom)

        # Niet resizable
        self.resizable(False, False)

        self.datax = None
        self.datay = None
        self.stdy = None

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
        self.datax = datax
        self.datay = datay
        self.stdy = stdy

    def save_data(self):
        path = self.Entry_path.get()
        filename = self.Entry_filename.get()

        if path == "":
            path = "../data"

        data_arr = np.array([self.datax, self.datay, self.stdy]).T

        np.savetxt(path+"/"+filename+".txt", data_arr)

        notif = Saved_data_notif(self)
        notif.get_path(path, filename)
        notif.message()

    def destroy(self) -> None:
        self.__class__.alive = False
        return super().destroy()

class Saved_data_notif(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)

    def get_path(self, path, filename):
        self.path = path
        self.filename = filename

    def message(self):
        self.label = ttk.Label(master=self, text="Data saved to: "+self.path+"/"+self.filename+".txt")
        self.label.grid(row=0, column=0, sticky="NSEW", columnspan=1,
                        rowspan=1)
