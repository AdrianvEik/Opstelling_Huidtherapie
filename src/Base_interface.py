
# Dit gaat een basis class vormen die kunnen worden gelinked aan
# classes in physics_interface.py en Student_Interface.py

import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk

from threading import Thread
from queue import Queue

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from src.Physics_Interface.Physics_interface import Base_physics
from src.Student_Interface.Student_interface import Student_start_measurement

class Base_interface(tk.Tk):
    """
    Base interface voor de GUI's

    Link in programma:

    Base -> Student_startup -> Student_load -> Student_results
    Base -> Physics_interface -\> student_load -> Physics_results -\> Student_results

    -> sluit na het laden van de volgende interface/indrukken knop
    -\> sluit NIET na het laden van de volgende interface/indrukken knop

    attributes:


    """
    def __init__(self):
        super().__init__()
        # Titel boven de GUI
        self.title("UV-huidtherapie")
        # self.frame = tk.Frame(self)
        # self.frame.grid()

        # Grid config, maar een kolom dus gewicht 1
        self.grid_columnconfigure(0, weight=1)

        # Grootte van de GUI in px
        self.geometry("500x500")

        # Niet resizable
        self.resizable(False, False)

        # Global row counter
        self.row = 0

        # Vars
        # Link naar het volgende scherm (student)
        self.student_startup = Student_start_measurement
        # Link naar het volgende scherm (physics)
        self.physics_link = Base_physics

        # Build GUI
        self.build_gui()

        # Voor alle rijen de gewichten aanpassen
        for i in range(self.row):
            self.grid_rowconfigure(i, weight=1)


    def student_button(self, linked_event):
        def on_action():
            from Physics_Interface.Physics_interface import generate_data, single_data

            st = self.student_startup()
            st.data_source = generate_data
            st.data_source_single = single_data

            st.measure_frame(st.verification_measurement,
                             result_function=st.update_startup)
            self.destroy()



        button = tk.Button(self, text="Student", command=on_action)
        # Pas pad aan voor positie en niet col of row
        button.grid(row=self.row, column=0, sticky="nsew", padx=50, pady=50)
        self.row += 1

    def physics_button(self, linked_event):
        def on_action():
            linked_event()
            self.destroy()

        button = tk.Button(self, text="Physics", command=on_action)
        # Pas pad aan voor positie en niet col of row
        button.grid(row=self.row, column=0, sticky="nsew", padx=50, pady=50)
        self.row += 1

    def build_gui(self):
        self.student_button(
            linked_event=self.student_startup
        )
        self.physics_button(
            linked_event=self.physics_link
        )
