
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
data_set_1_sensor = Fileread(folder+"/set1", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_nulmeting = Fileread(folder+"/nulmeting", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()

data_set_1_sensor = np.array(list(data_set_1_sensor.values()))
data_nulmeting = np.array(list(data_nulmeting.values()))

# Each 1st row is the voltage, each 2nd row is the time
# Each third row is the standard deviation

voltages_set1 = data_set_1_sensor[1:-1:3, :]
voltages_nulmeting = data_nulmeting[1:-1:3, :]
std = [np.std(voltages_set1[i]) * sigma for i in range(voltages_set1.shape[0])]

OD_values = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 2, 3, 4])
OD_values_hoog = np.array([2, 3, 4])

OD_values = OD_values

# Each voltage set is coupled to an OD value

avg_voltage_set12 = calculate_intesnity(np.average(voltages_set1, axis=1))
avg_nulmeting = calculate_intesnity(np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])])))


# Calculate the OD values
transmission_setthorlabs = np.abs(avg_voltage_set12 / avg_nulmeting)

OD_setthorlabs = -np.log10(transmission_setthorlabs)

folder = "230623_onzesensor/Met_versterking"
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
std = [np.std(voltages_set1[i]) * sigma for i in range(voltages_set1.shape[0])]

OD_values = np.array([0.1, 0.2, 0.3, 0.4, 0.6, 1, 2, 3, 4])
OD_values_hoog = np.array([2, 3, 4])

OD_values = OD_values

# Each voltage set is coupled to an OD value
avg_nulmeting = np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])]))


# Calculate the OD values
transmission_set1 = np.abs(avg_voltage_set12 / avg_nulmeting)

OD_set1 = -np.log10(transmission_set1)

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
print(avg_voltage_set12.shape)
# Add the data sets together and calculate the standard deviation
std = [np.std(voltages_set1[i]) * sigma for i in range(voltages_set1.shape[0])]

OD_values = np.array([0.1, 0.2, 0.3, 0.4, 0.6, 1, 2, 3, 4])
OD_values_hoog = np.array([2, 3, 4])


# Each voltage set is coupled to an OD value
avg_nulmeting2 = np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])]))


# Calculate the OD values
transmission_set2 = np.abs(avg_voltage_set12 / avg_nulmeting)
OD_set2 = -np.log10(transmission_set2)

OD_set1 = np.delete(OD_set1, 4)
OD_setthorlabs = np.delete(OD_setthorlabs, 4)

pl1 = Default(OD_values, OD_set2 - OD_set1, data_label="ML8511 UV versterkt - niet versterkt", colour="b", linestyle="",
              x_label="OD filter waarde", y_label="Verschil in OD-waarde", legend_loc="lower right",
              save_as="difference_versterkt.png", capsize=5, decimal_comma=False, marker="o")

pl2 = Default(OD_values, OD_set2 - OD_setthorlabs, data_label="ML8511 UV versterkt - Thorlabs sensor", colour="r", linestyle="",
              x_label="OD filter waarde", y_label="Verschil in OD-waarde", legend_loc="lower right",
              save_as="difference_versterkt.png", capsize=5, decimal_comma=False, add_mode=True, marker="*")

pl3 = Default(OD_values, OD_set1 - OD_setthorlabs, data_label="ML8511 UV niet versterkt - Thorlabs sensor", colour="g", linestyle="",
              x_label="OD filter waarde", y_label="Verschil in OD-waarde", legend_loc="lower right",
              save_as="difference_versterkt.png", capsize=5, decimal_comma=False, add_mode=True, marker="X")

pl1 += pl2
pl1 += pl3
pl1()