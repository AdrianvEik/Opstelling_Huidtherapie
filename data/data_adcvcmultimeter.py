
import matplotlib.pyplot as plt
import numpy as np

from AdrianPack.Fileread import Fileread
from AdrianPack.Aplot import Default

def fit_func(x, a):
    return a * x

def calculate_intesnity(x):
    # https://learn.sparkfun.com/tutorials/ml8511-uv-sensor-hookup-guide/all
    # Linear equation between 0 and 15mW/cm^2 and 1 and 3 V output
    return (x-0.99) * 15/2 + 1

sigma = 1

folder = "230623_thorlabs"

data_set_1_sensor = Fileread(folder+"/set2", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_nulmeting = Fileread(folder+"/nulmeting", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()

data_set_1_sensor = np.array(list(data_set_1_sensor.values()))
data_nulmeting = np.array(list(data_nulmeting.values()))

voltages_set1 = data_set_1_sensor[1:-1:3, :]
avg_voltage_set12 = calculate_intesnity(np.average(voltages_set1, axis=1))
voltages_nulmeting = calculate_intesnity(data_nulmeting[1:-1:3, :])

# Add the data sets together and calculate the standard deviation
std = [np.std(voltages_set1[i]) * sigma for i in range(voltages_set1.shape[0])]
OD_values = np.array([1, 2, 3, 4])

avg_nulmeting = np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])]))

# Calculate the OD values
transmission_set1 = np.abs(avg_voltage_set12 / avg_nulmeting)
OD_set1 = -np.log10(transmission_set1)


data_OD4 = np.array([0.0462, 0.0466, 0.0458, 0.0457, 0.0461, 0.0443, 0.0450, 0.0438, 0.0426, 0.0423])
avg_OD4, std_OD4 = np.average(data_OD4), np.std(data_OD4)
data_OD3 = np.array([0.0673, 0.0687, 0.0671, 0.0672, 0.0682, 0.0699, 0.0655, 0.0692, 0.0673, 0.0692])
avg_OD3, std_OD3 = np.average(data_OD3), np.std(data_OD3)
data_OD2 = np.array([0.0655, 0.0680, 0.0666, 0.0679, 0.0660, 0.0672, 0.0659, 0.0675, 0.0662, 0.0670])
avg_OD2, std_OD2 = np.average(data_OD2), np.std(data_OD2)
data_OD1 = np.array([0.1501, 0.1500, 0.1492, 0.1503, 0.1502, 0.1501, 0.1500, 0.1490, 0.1492, 0.1497])
avg_OD1, std_OD1 = np.average(data_OD1), np.std(data_OD1)

multimetermeas = np.array([avg_OD1, avg_OD2, avg_OD3, avg_OD4])
multimetermeas_std = np.array([std_OD1, std_OD2, std_OD3, std_OD4])
errmulti = multimetermeas_std / (multimetermeas * np.log(10))

transmission_multimeter = np.abs(multimetermeas / avg_nulmeting)
OD_multimeter = -np.log10(transmission_multimeter)

err = std / (OD_set1 * np.log(10))
# err[0] = np.log10(1 + std[0]/2) - np.log10(1 - std[0]/2)

pl = Default(OD_values, OD_set1, y_err=err, data_label="ADC", colour="b", linestyle="",
              x_label="OD filter waarde", y_label="OD gemeten waarde", capsize=5,
              legend_loc="lower right", save_as="ADCmultimeterthorlabs.png", marker="o", decimal_comma=False, fx=fit_func, func_format="fit lin. gebied: y = {0}x")
pl1 = Default(OD_values, OD_multimeter, y_err=errmulti, data_label="Multimeter", colour="r", linestyle="", capsize=5,
              legend_loc="lower right", marker="X", decimal_comma=False, add_mode=True, fx=fit_func, func_format="fit lin. gebied: y = {0}x")

pl += pl1
pl()