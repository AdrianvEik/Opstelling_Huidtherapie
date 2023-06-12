
from time import sleep
from typing import Tuple, List
import configparser as cp
import os


import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Hier iets wat voor nu data genereert om aan te leveren aan Base_interface
# Dit is een test functie
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
        self.config_path = os.path.join(os.path.dirname(__file__), "cfg.config")

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

        # Read the config and update the vars
        self.initialise_config_data()

        # Settings link
        self.settings_link = Settings
        self.settings_open = None

        ## Build GUI
        # Figsize
        self.dpi = 100
        self.figsize = (self.geom[0]/(2*self.dpi), self.geom[1]/(self.dpi))
        self.graph_topleft(generate_data())

        # Build the right side of the GUI

        # Updated real time data
        upd, vals = self.data_box([["Voltage", "Gemmidelde waarde", "Resultaat"], ["Label 2", "label 21", "label 22", "label 23"]],
                        [["0", "1", "2", "3"], ["0", "1", "2", "3"]],
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
                       ["Data opslaan", "Meet instellingen aanpassen", "Grafiek opslaan"]],
                      [["Laad", "Start", "Stop"], ["Opslaan", "Instellingen", "Opslaan"]],
                      "Hieronder staan enkele knoppen voor data verwerking.",
                      buttons=True,
                      commands=[[self.load_data, self.start_meas, self.pause_meas],
                                [self.load_data, self.start_settings, self.results]])
        self.job = self.update_vars(generate_data, [str(np.random.randint(10)) for i in range(6)])

    def initialise_config_data(self):
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
        pass

    def graph_topleft(self, data):
        """
        Graph in the top left corner
        """

        # Maak een figuur aan
        fig = plt.Figure(figsize=self.figsize, dpi=100)
        fig.suptitle("Test")

        # Maak een subplot aan
        ax = fig.add_subplot(111)
        # Maak een plot aan
        ax.plot(*data)
        # Maak een canvas aan
        canvas = FigureCanvasTkAgg(fig, master=self)
        # Laat de canvas zien
        canvas.draw()
        # Plaats de canvas in de GUI
        self.rowfig = 0
        canvas.get_tk_widget().grid(row=self.rowfig, column=0, sticky="NSEW", padx=10, pady=10,
                                    columnspan=3, rowspan=6)

        # self.after(1000, self.update, generate_data())
        return None

    def data_box(self, txt_labels: List[List[str]], entries: List[List[str or float]], explain_text: str, buttons: bool = False,
                 edit_state: bool = False, commands: List = None, updated: bool = False) -> List[tk.Entry] or None:
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
        label.grid(row=self.row, column=4, sticky="NSEW", columnspan=3, rowspan=1)
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
                if i % 2 ==0:
                    # Maak een label aan
                    try:
                        label = tk.Label(master=frame_data, text=txt_labels[labelnr][j])
                    except IndexError:
                        label = tk.Label(master=frame_data, text="")
                    # Plaats de label in het frame
                    label.grid(row=i, column=j, sticky="NSEW")
                else:
                    if buttons:
                        try:
                            button = tk.Button(master=frame_data, text=entries[entrnr][j], command=commands[entrnr][j])
                        except IndexError:
                            button = tk.Button(master=frame_data, text="", command=lambda x=0: None)
                        button.grid(row=i, column=j, sticky="NESW")
                        entries.append(button)
                    else:
                        try:
                            strvar = tk.StringVar(value=str(entries[entrnr][j]))
                            # strvar.trace("w", self.update_plc)
                        except IndexError:
                            strvar = tk.StringVar(value="")
                            # strvar.trace("w", self.update_plc)

                        # Maak een entry aan
                        entry = tk.Entry(master=frame_data, textvariable=strvar)
                        entry.setvar(str(strvar), str(entries[entrnr][j]))
                        entry.config(state="readonly" if not edit_state else "normal")
                        # Plaats de entry in het frame
                        entry.grid(row=i, column=j, sticky="NSEW")

                        if edit_state or buttons or updated:
                            entries.append(entry)
                            variables.append(strvar)

            if i % 2 == 0:
                labelnr += 1
            else:
                entrnr += 1

        frame_data.grid(row=self.row, column=4, sticky="NSEW", columnspan=1, rowspan=1)
        self.row += 1

        return (entries, variables) if (edit_state or buttons or updated) else None

    def update_vars(self, *args) -> str:
        """
        Update the variables in the GUI

        :param args[0]: Function that generates the data
        :param args[1]: Data points for all 6 boxes

        :return: None
        """
        if len(args) == 1:
            args = args[0]

        self.graph_topleft(args[0]())
        for en in range(len(self.vals)):
            self.vals[en].set(args[1][en])
            self.upd[en].config(state="normal")
            self.upd[en].setvar(str(self.vals[en]), str(self.vals[en].get()))
            self.upd[en].config(state="readonly")

        job = self.after(1000, self.update_vars, [generate_data, [str(np.random.randint(10)) for i in range(6)]])

        return job

    def get_data(self):
        # This function should be called to request data from the hardware.py file
        # And format it to be used in the graph/real time data

        # This is a placeholder

        # Wellicht functie als dit in hardware.py?
        # return should contain (tijd, data, avg, hardware informatie [voltage, laatst gelezen waarde, int value, etc.])
        return None


    def load_data(self):
        print("ld")
        return "data loaded"

    def save_data(self):
        print("sd")
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
        if self.job is not None:
            # Zoek de exacte job en stop deze met after_cancel
            self.after_cancel(self.call("after", "info")[0])
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
            self.job = self.update_vars(generate_data, [str(np.random.randint(10)) for i in range(6)])

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

class Settings(tk.Tk):

    def __int__(self):
        super().__int__()

        # Titel boven de GUI
        self.title("Technisch interface")

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
        label.grid(row=framerow, column=0, sticky="NSEW", columnspan=1, rowspan=1)
        entry = tk.Entry(master=frame)
        entry.grid(row=framerow, column=1, sticky="NSEW", columnspan=1, rowspan=1)
        framerow += 1

        frame.grid(row=self.row, column=0, sticky="NSEW", columnspan=1, rowspan=1)
        self.row += 1

class LoadData(tk.Tk):

    def __int__(self):
        pass