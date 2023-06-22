import sys
from time import sleep, time
from typing import Tuple, List
import configparser as cp
import threading
import queue

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

# Import the various windows
from src.Physics_Interface.Physics_interface_Settings import Settings
from src.Physics_Interface.Physics_interface_DataManipulation import SaveData
from src.Student_Interface.Student_interface import Student_start_measurement

global number_of_samples
try:
    from Hardware import ADCReader
    adc_reader = ADCReader()
    # Hier iets wat voor nu data genereert om aan te leveren aan Base_interface
    # Dit is een test functie
    def generate_data(samples, meastime=0.01) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genereer data voor de GUI

        :return: tijd, data
        """
        global adc_reader
        # Maak een array aan van data over de tijd, sleep is om te simuleren dat het even duurt
        nmeasurements = samples  # n nr of meas


        data_arr = np.zeros([nmeasurements, 3])
        for i in range(nmeasurements):
            d, t, s = adc_reader.get_meas(1, meastime, start_time=0)
            data_arr[i] = np.array([d, t, s])
        # Return tijd, data
        return data_arr[:, 1], data_arr[:, 0]

    def single_data(tref: float):
        global adc_reader
        return time(), adc_reader.voltage

except Exception as e:

    def generate_data(samples, meastime: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genereer data voor de GUI
        :return: tijd, data
        """
        # Maak een array aan van data over de tijd, sleep is om te simuleren dat het even duurt

        nmeasurements = samples  # n nr of meas
        # meastime t per meas

        data_arr = np.zeros([nmeasurements, 3])

        for i in range(nmeasurements):
            d, t, s = np.random.randint(0, 7), time(), np.random.randint(0, 100)
            sleep(meastime)
            data_arr[i] = np.array([d, t, s])

        return data_arr[:, 1], data_arr[:, 0]

    def single_data(tref):
        return np.array([time(), np.random.randint(0, 7)], dtype=float)



class Base_physics(tk.Tk):
    """
    Eerste start scherm, alles wat direct wordt gebruikt kan niet na instantiatie worden aangepast
    maar zou direct in de code moeten worden aangepast. Deze waarden staan dus
    gehardcode in de code.
    """
    def __init__(self):
        super().__init__()

        self.queue = queue.Queue()
        self.thread = None

        self.config_path = "../src/cfg_variable.config"
        """Pad naar configuratie bestand, wordt direct in de __init__ gebruikt"""

        self.title("Technisch interface")

        self.geom = (900, 600)
        """Geometrie van het scherm, wordt direct in de __init__ gebruikt"""

        self.geometry("%sx%s" % self.geom)

        # Niet resizable
        self.resizable(False, False)

        self.row = 0
        """Row counter voor de rechter helft, wordt gebruikt om de positie van de widgets te bepalen"""

        self.rowfig = 0
        """Row counter voor de linker helft, wordt gebruikt om de positie van het figuur te bepalen"""


        self.time_start = time()
        """Referentie tijd die van self.data_time wordt afgehaald om naar seconden te rekenen"""

        self.tref = 0

        ## Vars
        # Algemeen
        self.measurementtype = None
        """Type meting uit de config, 0 is een meting van N-punten 1 is een conitinue meting"""

        self.nrofmeasurements = None
        """Aantal metingen per meetserie voor meettype 0"""

        # Grafiek
        self.msperframe = None
        """Verversingstijd van de grafiek in ms"""

        self.xastype = None
        """Type van de x-as, 0 is tijd, 1 is samples"""
        self.yastype = None
        """Type van de y-as, 0 is spanning, 1 is intensiteit, 2 is transmissie, 3 is OD-waarde"""

        # RTdata
        self.msperdata = None
        """Verversingstijd van de realtime data in ms"""

        # Vaste parameters
        self.std = None
        """Standaarddeviatie van de metingen in std * sigma"""
        self.path2ref = None
        """Pad naar het referentie bestand"""

        # Student parameters
        self.nrofmeasurementsstudent = None
        """Aantal metingen per meetserie"""
        self.student_measurementtime = None
        """Tijd tussen metingen voor een studentmeting"""
        self.student_measurementtype = None
        """Type meting uit de config, 0 is een meting met als resultaat transmissie en 1 met OD waarde"""
        self.student_meas_marge = None
        """Marge voor de verificatie meting voordat een student meting is gestart"""

        # Initialise base data arrays
        shape = 1000
        self.xaxis = self.data_time = np.zeros(1)
        """Tijd array voor data verwerking en plotten"""
        self.yaxis = self.data_voltage = np.zeros(1)
        """Voltage array voor data verwerking en plotten"""

        self.student_voltage = np.zeros(shape)
        """Voltage array voor student metingen, wordt gebruikt voor dataanlyse van meest recente data"""
        self.student_time = np.zeros(shape)
        """Tijd array voor student metingen, wordt gebruikt voor dataanlyse van meest recente data"""
        self.prev_student_voltage = np.zeros(shape)
        self.prev_student_time = np.zeros(shape)

        # Read the config and update the vars
        self.initialise_config_data() # Update config variables
        self.read_student_measurement() # Update student measurement data arrays

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


    def Build_GUI_physics(self, updated=True):
        """"
        Bouw de GUI op en voeg de volgende elementen toe:
            - De linker helft van het scherm wordt opgevuld met een grafiek
              dit wordt gedaan met de functie ..py:class Base_physics.graph_topleft
            - De rechter helft van het scherm wordt opgevuld met een aantal
              'tabellen' met meetwaarden en resultaten van de realtime data
              en de meest recente student meting (die is opgeslagen in een file)
        De tabellen worden gemaakt met de functie ..py:class Base_physics.data_box

        :param updated: True om de update job te starten aan het einde van het opbouwen van de GUI. Voor bugfixing
        :type updated: bool

        :return: None
        """

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
        upd_st, vals_st = self.data_box([["Voltage", "Gemmidelde waarde", "Resultaat"],
                        ["UV-index", "Transmissie", "OD-waarde"]],
                      [["0", "1", "2", "3"], ["0", "1", "2", "3"]],
                      "Resultaten studentmeting", updated=True)

        self.upd_st = upd_st[2:]
        self.vals_st = vals_st

        # Buttons
        self.data_box([["Reset data", "Meting verichten", "Meting stoppen"],
                       ["Data opslaan", "Meet instellingen aanpassen",
                        "Student meting starten"]],
                      [["Reset", "Start", "Stop"],
                       ["Opslaan", "Instellingen", "Start"]],
                      "Hieronder staan enkele knoppen voor data verwerking.",
                      buttons=True,
                      commands=[
                          [self.reset_data, self.start_meas, self.pause_meas],
                          [self.save_data, self.start_settings, self.start_student_measurement]])

        self.thread = threading.Thread(target=self.measurement_thread, args=(
                                        self.queue, self.time_start, self.measurementtype,
                                        self.nrofmeasurements, self.data_time[-1], self.data_time,
                                        self.data_voltage, float(self.msperframe)/(float(self.nrofmeasurements)*1000)))

        if updated:
            self.thread.start()
            self.job = self.update_vars(self.read_ndatapoints(), self.update_student_measurement())

        return None

    # Configuratie methods
    def initialise_config_data(self) -> None:
        """
        Lees de config file ui, het pad hiernaartoe is eerder gedefinieerd
        en hard coded om te voorkomen dat er problemen ontstaan met het
        vinden en uitlezen van de config file.

        :return: None
        """
        config = cp.ConfigParser()
        config.read(self.config_path)
        # 0 = 1 frame voor x aantal metingen, 1 = real time toevoeging van metingen tot x aantal metingen dan
        # verversen van grafiek
        self.measurementtype = config["Algemeen"]["typemeting"]
        self.nrofmeasurements = config["Algemeen"]["nmetingen"]

        self.msperframe = config["Grafiek"]["MsPerFrame"]

        # x-as: 0 = tijd, 1 = metingen
        self.xastype = config["Grafiek"]["Grafiektypex"]
        # y-as: 0 = voltage, 1 = intensiteit, 2 = transmissie ,3 = OD
        self.yastype = config["Grafiek"]["Grafiektypey"]

        self.msperdata = config["RTData"]["MsPerData"]

        self.std = config["VasteParameters"]["std"]
        self.path2ref = config["VasteParameters"]["path_to_ref"]

        self.nrofmeasurementsstudent = config["StudentMeting"]["measurement"]
        self.student_measurementtime = config["StudentMeting"]["measurement_time"]
        self.student_measurementtype = config["StudentMeting"]["measurement_type"]
        self.student_meas_marge = config["StudentMeting"]["marge_student_verify"]

    def savecfg_to_config(self):
        """
        Converteer alle variabelen naar een config met de ConfigParser module
        en schrijf deze weg naar de variabele config.

        :return: None
        """
        config = cp.ConfigParser()
        # 0 = 1 frame voor x aantal metingen, 1 = real time toevoeging van metingen tot x aantal metingen dan
        # verversen van grafiek
        config["Algemeen"] = {"typemeting": self.measurementtype,
                                "nmetingen": self.nrofmeasurements}

        config["Grafiek"] = {"MsPerFrame": self.msperframe,
                               "Grafiektypex": self.xastype,
                                 "Grafiektypey": self.yastype}


        config["RTData"] = {"MsPerData": self.msperdata}

        config["VasteParameters"] = {"std": self.std,
                                        "path_to_ref": self.path2ref}

        config["StudentMeting"] = {"measurement": self.nrofmeasurementsstudent,
                                       "measurement_time": self.student_measurementtime,
                                         "measurement_type": self.student_measurementtype,
                                           "marge_student_verify": self.student_meas_marge}

        with open(self.config_path, "w") as config_file:
            config.write(config_file)


    def read_student_measurement(self):
        """
        Lees het pad met de student meting uit, hardcoded. Als er geen verandering
        in de data is, return dan False, anders return True.

        :return: Wel of geen verandering in de data
        :rtype: bool
        """
        self.prev_student_time = self.student_time
        self.prev_student_voltage = self.student_voltage
        data = np.loadtxt("MeestRecenteMeting.txt", delimiter=" ")
        self.student_voltage = data[:, 1]
        self.student_time = data[:, 0]

        return np.all(np.abs(self.student_time - self.prev_student_time) < 0.001)


    # Frames en opbouw van de GUI
    def graph_topleft(self):
        """
        Maak een grafiek en plaats deze in de linkerhelft van de GUI.
        De grafiek is een animatie om de data real time te kunnen plotten. Deze
        animatie wordt aangestuurd door de functie self.animate().

        :return: None
        """

        # Maak een figuur aan
        self.fig = plt.Figure(figsize=self.figsize, dpi=100)
        # self.fig.suptitle("Test")

        # x-labels
        x_labels = ["Tijd $t$ [s]", "Metingen $n$ [-]"]
        y_labels = ["Voltage $V$ [V]", "Intensiteit $I$ [mW/cm$^2$]", "Transmissie $T$ [-]", "Optische dichtheid $OD$ [-]"]

        # Maak een subplot aan
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True, axis="y")

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
        """
        Functie die de data van de grafiek update. De data wordt uit de attributes
        self.xaxis en self.yaxis gehaald welke worden geupdate door de functie
        self.update_vars().
        :param i:
        :return:
        """
        self.line.set_xdata(self.xaxis)
        self.line.set_ydata(self.yaxis)

        min_x, max_x = min(self.xaxis), max(self.xaxis)
        min_y, max_y = min(self.yaxis), max(self.yaxis)


        self.ax.set_xlim(min_x - 0.01, max_x + 0.01)

        self.ax.set_ylim(min_y - 0.5, max_y + 0.5)

        return self.line,

    def data_box(self, txt_labels: List[List[str]],
                 entries: List[List[str or float]], explain_text: str,
                 buttons: bool = False,
                 edit_state: bool = False, commands: List = None,
                 updated: bool = False) -> List[tk.Entry] or None:
        """
        Een tabel met 2x3 entries en hieraan een label met uitleg, boven de box
        met entries/labels staat een label met uitleg welke ook meegegeven kan
        worden. De entries kunnen ook buttons zijn met een gekoppelde command.

        Voorbeeld om de variabelen verder in het script te kunnen updaten:

        .. code-block:: python

            for entry in range(len(stringvars)):
                stringvars[en].set(stringvars[entry]) # Update de stringvars
                # configureer de entries om nieuwe waarden te accepteren
                entries_list[en].config(state="normal")
                # Vul de nieuwe waarden van de stringvar in in de entries
                entries_list[en].setvar(str(stringvars[en]), str(stringvars.get()))
                # Maak de entries weer readonly
                entries_list.config(state="readonly")


        :param txt_labels: Lijst van labels voor de entries gegeven als [[labels van row 1], [labels van row 2]]
        :type txt_labels: List[List[str]]

        :param entries: Lijst van, standaard ingevulde waarden, voor de entries in het zelfde format als txt_labels deze kunen geupdate worden als updated True is.
        :type entries: List[List[str or float]]

        :param buttons: True als de entries buttons moeten zijn, hierbij wordt de entries parameter gebruikt als de labels weergegeven in de entry.
        :type buttons: bool

        :param edit_state: True als de entries aangepast moeten kunnen worden, False als de entries niet aangepast mogen worden. Hierbij kan user input gevraagd worden.
        :type edit_state: bool

        :param updated: True als de entries geupdate moeten kunenn worden via de entries en stringvars die worden meegegeven in de return, False als de entries niet geupdate moeten worden.

        :param commands: Alleen van toepassing als buttons True is, dit is een lijst van commando's die gekoppeld zijn aan de buttons in hetzelfde format als txt_labels en entries.
        :type commands: List[List[Callable]]

        :return: In het geval dat edit_state, update of buttons true is worden de signatures van de entries en de tk.StringVar van de ingevulde waardes teruggegeven.
        :rtype: Tuple[List[tk.Entry], List[tk.StringVar]] or None

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
        Verwerk de binnengekomen data van de ADC die in de self.data_voltage
        en bereken hiermee de transmissie, intensiteit en OD waarde. Voor
        de OD waarde en transmissie wordt de referentie file gebruikt die staat
        gespecificeerd in de instellingen. De return is 6 strings voor de
        data_box.

        Lijst van strings:
         - Laasts gemeten voltage
         - Gemiddelde voltage +- standaard deviatie
         - Intensiteit (via ..python:func:`calculate_intesnity`)
         - Transmissie (gemeten intensiteit/ ref intensiteit)
         - OD waarde (log10(1/transmissie))

        :return: Een lijst van strings met de waardes van voltage, transmissie, intensiteit en OD waarde.
        :rtype: List[str]
        """
        avg, std = np.average(self.data_voltage), np.std(self.data_voltage) * int(self.std)
        transmissie = avg/self.refavg

        return ["{:>5.6f}".format(self.data_voltage[-1]),
                "{:>5.6f} ± {:>5.4f}".format(avg, std),
                "{:>5.6f}".format(self.calculate_intesnity(avg)),
                str(0), transmissie, np.log10(1/transmissie)]

    def update_student_measurement(self):
        avg, std = np.average(self.student_voltage), np.std(self.student_voltage) * int(self.std)
        transmissie = avg/self.refavg

        return ["{:>5.6f}".format(self.student_voltage[-1]),
                "{:>5.6f} ± {:>5.4f}".format(avg, std),
                "{:>5.6f}".format(self.calculate_intesnity(avg)),
                str(0), transmissie, np.log10(1/transmissie)]

    def measurement_thread(self, q, tstart, measurementtype, nrofmeasurements,
                           last_time, prev_data_time, prev_data_voltage,
                           meas_time=0.01):
        if measurementtype == str(0):
            data_time, data_voltage = generate_data(
                int(nrofmeasurements), meas_time)
            data_time -= tstart
        else:
            data = single_data(last_time)

            if prev_data_time.shape[0] > 200:
                data_time, data_voltage = prev_data_time[1:], prev_data_voltage[1:]
                data_time[-1] = data[0] - tstart
                data_voltage[-1] = data[1]

            else:
                data_time = np.append(prev_data_time, data[0] - tstart)
                data_voltage = np.append(prev_data_voltage, data[1])

        intensity = self.calculate_intesnity(data_voltage)

        q.put([data_time, data_voltage, intensity])
        return None

    # Real time data verwerking en after methode
    def update_vars(self, *args) -> str:
        """
        Functie die iedere 1000ms wordt aangeroepen en de data van de ADC
        verwerkt en de data boxen/grafiek update. Eerst worden alle variablen
        geupdate in de data boxen vervolgenswordt de as berekend a.d.h.v. de
        self.data_voltage en de self.data_time en gegeven instellingen uit config.

        Volgorde van verloop:

        1. Lees de meest recente studentmeting uit, 'MeesteRecenteMeting.txt'
        2. Voor alle 6 de data entries in de recente meting en student box wordt de waarde geupdate volgens de volgorde in *args
        3. Verwerk de data uit de meest recente meting naar behoren van instellingen voor de x-as en y-as
        4. Roep de functie voor het updaten van de plot in de grafiek aan
        5. Roep recursief deze functie aan iedere 1000ms

        :param args[0]: Lijst met verwerkte meest recente data uitgelezen uit de ADC
        :param args[1]: Lijst met meest recent ingelezen data uit de studentmeting

        :return: De naam van de Job aangemaakt via deze functie
        :rtype: str
        """
        if len(args) == 1:
            args = [args[0]]

        if self.read_student_measurement():  # TODO: nagaan of dit echt sneller is dan iedere keer updaten
            for en in range(len(self.vals)):
                self.vals_st[en].set(args[1][en])
                self.upd_st[en].config(state="normal")
                self.upd_st[en].setvar(str(self.vals_st[en]),
                                       str(self.vals_st[en].get()))
                self.upd_st[en].config(state="readonly")

        if self.thread.is_alive():
            pass
        else:
            try:
                data_time, data_voltage, intensity = self.queue.get(block=False)

                self.data_time = data_time
                self.data_voltage = data_voltage
            except queue.Empty:
                pass

            data_time_axis = self.data_time
            data_voltage_axis = self.data_voltage

            if self.xastype == str(0):
                data_time_axis = self.data_time
            elif self.xastype == str(1):
                data_time_axis = list(range(len(self.data_time)))

            if self.yastype == str(0):
                data_voltage_axis = self.data_voltage
            elif self.yastype == str(1):
                data_voltage_axis = intensity
            elif self.yastype == str(2):
                data_voltage_axis = self.calculate_intesnity(self.data_voltage)/self.refavg
            elif self.yastype == str(3):
                data_voltage_axis = np.log10(np.abs(self.refavg/self.calculate_intesnity(self.data_voltage)))

            self.xaxis = data_time_axis
            self.yaxis = data_voltage_axis

            # self.graph_topleft(args[0]())
            for en in range(len(self.vals)):
                self.vals[en].set(args[0][en])
                self.upd[en].config(state="normal")
                self.upd[en].setvar(str(self.vals[en]), str(self.vals[en].get()))
                self.upd[en].config(state="readonly")

            self.thread = threading.Thread(target=self.measurement_thread,
                                           args=(self.queue, self.time_start,
                                                 self.measurementtype, self.nrofmeasurements,
                                                 self.data_time[-1], self.data_time,
                                                 self.data_voltage,
                                                 float(self.msperframe)/(float(self.nrofmeasurements)*1000)))
            self.thread.start()

        job = self.after(self.msperdata, self.update_vars,
                         self.read_ndatapoints(), self.update_student_measurement())  # 1000ms = 1s

        return job

    # Gelinkte functies
    def calculate_intesnity(self, x):
        # https://learn.sparkfun.com/tutorials/ml8511-uv-sensor-hookup-guide/all
        # Linear equation between 0 and 15mW/cm^2 and 1 and 3 V output
        return (x-0.99) * 15/2 + 1

    def reset_data(self):

        self.pause_meas()
        self.queue.queue.clear()

        self.xaxis = self.data_time = np.zeros(1)
        self.yaxis = self.data_voltage = np.full(1, self.data_voltage[-1])

        self.time_start = time()

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

            self.thread.join()

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
            self.job = self.update_vars(self.read_ndatapoints(), self.update_student_measurement())

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

        st = Student_start_measurement()
        st.data_source = generate_data
        st.data_source_single = single_data

        st.measure_frame(st.verification_measurement, result_function=st.update_startup)

    def destroy(self) -> None:
        self.pause_meas()
        self.fig.clear()

        try:
            super().destroy()
        except tk.TclError:
            sys.exit()

        return None




