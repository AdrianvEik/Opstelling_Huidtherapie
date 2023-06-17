
import tkinter as tk
import numpy as np
from tkinter import ttk
import configparser as cp



class Settings(tk.Toplevel):
    alive = False

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Titel boven de GUI
        self.title("Instellingen")

        # Grootte van de GUI in px
        # self.geom = (400, 500)
        # self.geometry("%sx%s" % self.geom)

        # Niet resizable
        self.resizable(False, False)

        # Global row counter
        self.row = 0

        # Settings aanmaken
        self.build_settings()

        self.__class__.alive = True

    def get_config(self):
        return None

    def build_settings(self):
        frame = tk.Frame(master=self)
        framerow = 0
        # Maak een label aan
        label_algemeen = tk.Label(master=frame, text="Algemene instellingen")
        label_algemeen.grid(row=framerow, column=0, sticky="NSEW",
                            columnspan=2,
                            rowspan=1, padx=[0, 50])
        framerow += 1

        self.selectie_typmeet = tk.StringVar(frame)
        options_typmeet = ["N-samples", "Live sample additie"]

        label_typmeting = ttk.Label(master=frame, text="Meting type")
        label_typmeting.grid(row=framerow, column=0, sticky="NSEW",
                             columnspan=1,
                             rowspan=1, padx=[0, 50])

        preset_option = "N-samples" if self.parent.measurementtype == str(0) else "Live sample additie"

        self.drop_typmeting = ttk.OptionMenu(frame, self.selectie_typmeet, preset_option,
                                       *options_typmeet)

        self.drop_typmeting.grid(row=framerow, column=1, sticky="NSEW",
                            columnspan=1,
                            rowspan=1)
        framerow += 1

        ndatapoints = tk.StringVar(frame)
        label_ndatapoints = tk.Label(master=frame, text="N-samples")
        label_ndatapoints.grid(row=framerow, column=0, sticky="NSEW",
                               columnspan=1,
                               rowspan=1, padx=[0, 50])

        self.Entry_ndatapoints = tk.Entry(master=frame, textvariable=ndatapoints)
        self.Entry_ndatapoints.insert(0, self.parent.nrofmeasurements)

        self.Entry_ndatapoints.grid(row=framerow, column=1, sticky="NSEW",
                               columnspan=1,
                               rowspan=1)
        framerow += 1

        # GRAFIEK INSTELLINGEN
        label_grafiek = tk.Label(master=frame, text="Grafiek instellingen")
        label_grafiek.grid(row=framerow, column=0, sticky="NSEW",
                            columnspan=2,
                            rowspan=1, padx=[0, 50])
        framerow += 1

        label_typmeting = ttk.Label(master=frame, text="x-as grafiek")
        label_typmeting.grid(row=framerow, column=0, sticky="NSEW",
                             columnspan=1,
                             rowspan=1, padx=[0, 50])

        self.selectie_grafiek_xas = tk.StringVar(frame)
        options_grafiek = ["Tijd", "Aantal metingen"]
        preset_selctie = "Tijd" if self.parent.xastype == str(0) else "Aantal metingen"
        self.drop_grafiek_xas = ttk.OptionMenu(frame, self.selectie_grafiek_xas, preset_selctie,
                                            *options_grafiek)
        self.drop_grafiek_xas.grid(row=framerow, column=1, sticky="NSEW",
                                columnspan=1,
                                rowspan=1)

        framerow += 1

        label_typmeting = ttk.Label(master=frame, text="y-as grafiek")
        label_typmeting.grid(row=framerow, column=0, sticky="NSEW",
                                columnspan=1,
                                rowspan=1, padx=[0, 50])


        self.selectie_grafiek_yas = tk.StringVar(frame)
        print(int(self.parent.yastype))
        options_grafiek = ["Spanning (V)", "Intensiteit", "Transmissie", "OD-waarde"]
        preset_selctie = "Spanning (V)" if self.parent.yastype == str(0) else "Intensiteit" if\
                            self.parent.yastype == str(1) else "Transmissie" if\
                            self.parent.yastype == str(2) else "OD-waarde"
        self.drop_grafiek_yas = ttk.OptionMenu(frame, self.selectie_grafiek_yas, preset_selctie,
                                            *options_grafiek)
        self.drop_grafiek_yas.grid(row=framerow, column=1, sticky="NSEW",
                                columnspan=1,
                                rowspan=1)

        framerow += 1

        label_vervmeting = ttk.Label(master=frame, text="Vervesingssnelheid metingen [ms]")
        label_vervmeting.grid(row=framerow, column=0, sticky="NSEW",
                                columnspan=1,
                                rowspan=1, padx=[0, 50])
        self.entry_vervmeting = tk.Entry(master=frame)
        self.entry_vervmeting.insert(0, self.parent.msperframe)
        self.entry_vervmeting.grid(row=framerow, column=1, sticky="NSEW",
                                columnspan=1,
                                rowspan=1)

        framerow += 1

        label_stapsgrootte = ttk.Label(master=frame, text="Stapsgrootte x-as")
        label_stapsgrootte.grid(row=framerow, column=0, sticky="NSEW",
                                columnspan=1,
                                rowspan=1, padx=[0, 50])
        self.entry_stapsgrootte = tk.Entry(master=frame)
        self.entry_stapsgrootte.insert(0, self.parent.stepsize)
        self.entry_stapsgrootte.grid(row=framerow, column=1, sticky="NSEW",
                                    columnspan=1,
                                    rowspan=1)

        framerow += 1

        # VASTE INSTELLINGEN
        label_vast = tk.Label(master=frame, text="Vaste instellingen")
        label_vast.grid(row=framerow, column=0, sticky="NSEW",
                            columnspan=2,
                            rowspan=1, padx=[0, 50])

        framerow += 1

        label_sigma_factor = ttk.Label(master=frame, text="Sigma factor")
        label_sigma_factor.grid(row=framerow, column=0, sticky="NSEW",
                                columnspan=1,
                                rowspan=1, padx=[0, 50])

        self.entry_sigma_factor = tk.Entry(master=frame)
        self.entry_sigma_factor.insert(0, self.parent.std)
        self.entry_sigma_factor.grid(row=framerow, column=1, sticky="NSEW",
                                    columnspan=1,
                                    rowspan=1)

        framerow += 1

        label_path2ref = ttk.Label(master=frame, text="Pad naar referentie")
        label_path2ref.grid(row=framerow, column=0, sticky="NSEW",
                                columnspan=1,
                                rowspan=1, padx=[0, 50])

        self.entry_path2ref = tk.Entry(master=frame)
        self.entry_path2ref.insert(0, self.parent.path2ref)
        self.entry_path2ref.grid(row=framerow, column=1, sticky="NSEW",
                                    columnspan=1,
                                    rowspan=1)


        framerow += 1

        button_save = ttk.Button(master=frame, text="Opslaan", command=self.save_options)
        button_save.grid(row=framerow, column=0, sticky="NSEW", columnspan=1,
                     rowspan=1)
        button_cancel = ttk.Button(master=frame, text="Reset", command=self.reset_options)
        button_cancel.grid(row=framerow, column=1, sticky="NSEW", columnspan=1,
                        rowspan=1)


        frame.grid(row=self.row, column=0, sticky="NSEW", columnspan=1,
                   rowspan=1)

        self.row += 1

    def save_options(self):
        self.parent.nrofmeasurements = str(self.Entry_ndatapoints.get())
        self.parent.measurementtype = str(0) if self.selectie_typmeet.get() == "N-samples" else str(1)

        self.parent.xastype = str(0) if self.selectie_grafiek_xas.get() == "Tijd" else str(1)
        sel_yas = self.selectie_grafiek_yas.get()
        self.parent.yastype = str(0) if sel_yas == "Spanning (V)" else str(1) if sel_yas == "Intensiteit" else str(2) if sel_yas == "Transmissie" else str(3)
        self.parent.msperframe = str(self.entry_vervmeting.get())
        self.parent.stepsize = str(self.entry_stapsgrootte.get())
        self.parent.std = str(self.entry_sigma_factor.get())
        self.parent.path2ref = self.entry_path2ref.get()

        self.row = 0
        self.build_settings()

        self.parent.pause_meas()
        self.parent.start_meas()
        return None

    def reset_options(self):
        config = cp.ConfigParser()
        config.read("../src/cfg_variable.config")
        self.parent.measurementtype = config["Algemeen"]["typemeting"]

        self.parent.nrofmeasurements = config["Algemeen"]["nmetingen"]

        self.parent.msperframe = config["Grafiek"]["MsPerFrame"]
        self.parent.xastype = config["Grafiek"]["Grafiektypex"]
        self.parent.yastype = config["Grafiek"]["Grafiektypey"]

        self.parent.stepsize = config["Grafiek"]["Stapsgrootte"]

        self.parent.msperdata = config["RTData"]["MsPerData"]

        self.parent.adc2v = config["VasteParameters"]["ADC2V"]
        self.parent.std = config["VasteParameters"]["std"]
        self.parent.path2ref = config["VasteParameters"]["path_to_ref"]

        self.row = 0
        self.build_settings()
        self.parent.pause_meas()
        self.parent.start_meas()

    def destroy(self) -> None:
        self.__class__.alive = False
        return super().destroy()