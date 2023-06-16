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
    uitlezen
    """

    def __init__(self):
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1015(self.i2c)

        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P1)

        # Create differential input between channel 0 and 1
        # self.chan = AnalogIn(self.ads, ADS.P0, ADS.P1)

    def read_adc(self):
        return self.chan.value, self.chan.voltage

    def get_meas(self, nmeas: int, tijd: float, sigma: int = 1,
                 start_time: float = 0) -> Tuple[np.ndarray, float]:
        meastime = tijd / nmeas
        measlist = []

        for i in range(nmeas):
            time.sleep(meastime)
            measlist.append(self.read_adc()[1])

        t = time.time() - start_time

        return np.average(measlist), t, np.std(measlist) * sigma

    def show_measure(self):
        while True:
            print(
                "{:>5}\t{:>5.3f}\t{:>5.6f}".format(*self.get_meas(1, 0.1, 3)))


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
        for i in range(nmeasurements):
            d, t, s = adc_reader.get_meas(25, meastime, start_time=tstart)
            data_arr[i] = np.array([d, t, s])
        np.savetxt(path, data_arr)

        return data_arr
