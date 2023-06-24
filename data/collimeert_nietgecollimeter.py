
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

folder = "data_onze_sensor"

data_set_1_sensor = Fileread(folder+"/set1", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_set_2_sensor = Fileread(folder+"/set2", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_nulmeting = Fileread(folder+"/nulmeting", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()

data_set_1_sensor = np.array(list(data_set_1_sensor.values()))
data_set_2_sensor = np.array(list(data_set_2_sensor.values()))
data_nulmeting = np.array(list(data_nulmeting.values()))

# Each 1st row is the voltage, each 2nd row is the time
# Each third row is the standard deviation

voltages_set1 = data_set_1_sensor[0:-1:3, :]
voltages_set2 = data_set_2_sensor[0:-1:3, :]
avg_voltage_set12 = calculate_intesnity(np.average(np.concatenate((voltages_set1, voltages_set2), axis=1), axis=1))
voltages_nulmeting = calculate_intesnity(data_nulmeting[0:-1:3, :])

# Add the data sets together and calculate the standard deviation
std = [np.std(np.concatenate([voltages_set1[i], voltages_set2[i]], axis=0)) * 3 for i in range(voltages_set1.shape[0])]

OD_values = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 2])
OD_values_hoog = np.array([2, 3, 4])

OD_values = OD_values

# Each voltage set is coupled to an OD value
avg_voltage_set12 = np.array([np.average(avg_voltage_set12[i]) for i in range(len(OD_values))])
avg_nulmeting = np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])]))


# Calculate the OD values
transmission_set1 = np.abs(avg_voltage_set12 / avg_nulmeting)

OD_setnietgecollimeerd = -np.log10(transmission_set1)

std = std / (OD_setnietgecollimeerd * np.log(10))

pl1 = Default(OD_values[:7], OD_setnietgecollimeerd[:7], y_err=std[:7], data_label="ML8511 UV niet gecollimeerd", colour="b", fx=fit_func, linestyle="",
              x_label="OD filter waarde", y_label="OD gemeten waarde", func_format="fit lin. gebied: y = {0}x",
              legend_loc="lower right", save_as="Gecollimeerd_vsniet.png", capsize=5, decimal_comma=False)
pl2 = Default(OD_values[7:], OD_setnietgecollimeerd[7:], y_err=std[7:], colour="b", linestyle="",
              add_mode=True, data_label="", capsize=5)

# Gecollimeerd
folder = "230623_onzesensor/zonder_versterking"

data_set_1_sensor = Fileread(folder+"/set1", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_nulmeting = Fileread(folder+"/nulmeting", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()

data_set_1_sensor = np.array(list(data_set_1_sensor.values()))
data_nulmeting = np.array(list(data_nulmeting.values()))

# Each 1st row is the voltage, each 2nd row is the time
# Each third row is the standard deviation

voltages_set1 = data_set_1_sensor[1:-1:3, :]
avg_voltage_set12 = calculate_intesnity(np.average(voltages_set1, axis=1))
voltages_nulmeting = calculate_intesnity(data_nulmeting[1:-1:3, :])

# Add the data sets together and calculate the standard deviation
std = np.array([np.std(voltages_set1[i]) * sigma for i in range(voltages_set1.shape[0])])

OD_values = np.array([0.1, 0.2, 0.3, 0.4, 0.6, 1, 2, 3, 4])
OD_values_hoog = np.array([2, 3, 4])

OD_values = OD_values

# Each voltage set is coupled to an OD value
avg_nulmeting = np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])]))

# Calculate the OD values
transmission_set1 = np.abs(avg_voltage_set12 / avg_nulmeting)
OD_set1 = -np.log10(transmission_set1)

std = std / (OD_set1 * np.log(10))

pl11 = Default(OD_values[:6], OD_set1[:6], y_err=std[:6], data_label="ML8511 UV gecollimeerd", colour="r", fx=fit_func, linestyle="",
              x_label="OD filter waarde", y_label="OD gemeten waarde", func_format="fit lin. gebied: y = {0}x",
              legend_loc="lower right", capsize=5, decimal_comma=False, add_mode=True)
pl21 = Default(OD_values[6:], OD_set1[6:], y_err=std[6:], colour="b", linestyle="",
              add_mode=True, data_label="", capsize=5)

pl1 += pl2
pl1 += pl11
pl1 += pl21

pl1()

# plt.savefig("data_thorlas/plot_ODOD.png", dpi=600)
