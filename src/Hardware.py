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

class ADCReader:
    def __init__(self):
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)
        
        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1015(self.i2c)
        
        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P0)
        
        # Create differential input between channel 0 and 1
        # self.chan = AnalogIn(self.ads, ADS.P0, ADS.P1)
    
    def read_adc(self):
        print("{:>5}\t{:>5}".format('raw', 'v'))
        while True:
            print("{:>5}\t{:>5.3f}".format(self.chan.value, self.chan.voltage))
            time.sleep(0.5)

# Create an instance of the ADCReader class
adc_reader = ADCReader()

# Start reading the ADC values
adc_reader.read_adc()

#You can create an instance of the ADCReader class and call the read_adc() method to start reading the ADC values. 
#The read_adc() method #will continuously print the raw ADC value and the corresponding voltage with a delay of 0.5 seconds between readings
