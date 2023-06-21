# Hier de code voor hardware aansturing van de raspberry pi
# pls alleen defs (of liever nog classes) hierin zetten en geen code
# testen kan met de main.py file of met de test_hardware.py file
# dit om de tests die gedaan zijn te behouden en te kunnen herhalen/documenteren
# klein tests kan in __main__ gedaan worden

# Note: dit moet volledig zelfstandig kunnen werken, dus geen imports van andere files
#       als je iets nodig hebt, zet het hierin of in een andere file in deze map

# Note: let op alle imports en beschrijf waar ze vandaan komen (als het niet
# python eigen of numpy/scipy is)

# Note: overal comments en docstrings plaatsen dit ivm de documentatie en
#       de leesbaarheid van de code

# Data wegschrijven naar ../test_data en NIET naar deze map of naar ../ (root)
# dit ivm de gitignore/versie beheer

import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


class ADCReader:
    """
    Class om de ADC uit te lezen
    """

    def __init__(self):
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        self.adc = ADS.ADS1015(self.i2c, gain=1)
        """De ADC die wordt uitgelezen"""

        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.adc, ADS.P1)
        """Channel waarop wordt uitgelezen"""

    @property
    def voltage(self) -> float:
        """
        Voltage dat uit de ADC wordt gelezen

        :return: voltage in V
        :rtype: float
        """
        v = self.chan.voltage

        # Hier code om voltage te manipuleren of vervangen zodat
        # deze het juiste voltage teruggeeft

        return v

    def get_meas(self, nmeas: int, tijd: float, sigma: int = 1,
                 start_time: float = 0) -> Tuple[float, float, float]:
        """
        Doe een meting van nmeas metingen met een totale tijd van tijd en
        een sigma van sigma. start_time is de tijd waarop de meting is gestart
        en wordt gebruikt om de timestamp van ieder punt te berekenen.

        :param nmeas: Het aantal metingen dat uitgevoerd en samengevoegd wordt
        :type nmeas: int
        :param tijd: De totale tijd van de meting
        :type tijd: float
        :param sigma: De sigma factor in de standaardeviatie I.E. 3*sigma
        :type sigma: int, optional
        :param start_time: De tijd waarop de meting is gestart. Default 0
        :type start_time: float
        :return: De gemiddelde waarde van de meting, de tijd van de meting en
                    de standaarddeviatie van de meting
        :rtype: Tuple[float, float, float]
        """
        meastime = tijd / nmeas
        measlist = []

        for i in range(nmeas):
            time.sleep(meastime)
            measlist.append(self.voltage)

        t = time.time() - start_time

        return float(np.average(measlist)), float(t), float(np.std(measlist) * sigma)

    def show_measure(self) -> None:
        """
        Laat de metingen zien in de console als:
            "nmeas\ttijd\tgemiddelde"

        :return: None
        """
        while True:
            print(
                "{:>5}\t{:>5.3f}\t{:>5.8f}".format(*self.get_meas(1, 0.1, 3)))


if __name__ == "__main__":
    # Create an instance of the ADCReader class
    adc_reader = ADCReader()


    # adc_reader.show_measure()

    # Start reading the ADC values
    def save_to_txt(path: str) -> np.ndarray:
        nmeasurements = 100  # n nr of meas
        meastime = 0.1  # t per meas

        tstart = time.time()

        data_arr = np.zeros([nmeasurements, 3])
        print("meting start!")
        for i in range(nmeasurements):
            d, t, s = adc_reader.get_meas(25, meastime, start_time=tstart)
            data_arr[i] = np.array([d, t, s])
        
        print("meting stopt!")

        np.savetxt(path, data_arr)

        return data_arr
    
    data = save_to_txt("../data/reference.txt")
    plt.errorbar(data[:, 1], data[:, 0], yerr=data[:, 2], fmt="ro", capsize=5)
    plt.show()
