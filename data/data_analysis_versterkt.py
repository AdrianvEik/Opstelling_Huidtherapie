
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

OD_values = OD_values

# Each voltage set is coupled to an OD value
avg_nulmeting = np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])]))


# Calculate the OD values
transmission_set1 = np.abs(avg_voltage_set12 / avg_nulmeting)
print(transmission_set1.shape)
OD_set1 = -np.log10(transmission_set1)
print(OD_set1.shape, OD_values.shape)
print(OD_set1[6:], OD_values[6:])
pl1 = Default(OD_values[:6], OD_set1[:6], y_err=std[:6], data_label="ML8511 UV zonder versterking", colour="b", fx=fit_func, linestyle="",
              x_label="OD filter waarde", y_label="OD gemeten waarde", func_format="fit lin. gebied: y = {0}x",
              legend_loc="lower right", save_as="ODOD_versterkt.png", capsize=5, decimal_comma=False)
pl2 = Default(OD_values[6:], OD_set1[6:], y_err=std[6:], colour="b", linestyle="",
              add_mode=True, data_label="", capsize=5)

pl1 += pl2

# Second dataset
folder = "230623_thorlabs"
data_set_1_sensor = Fileread(folder+"/set1", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_nulmeting = Fileread(folder+"/nulmeting", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()

data_set_1_sensor = np.array(list(data_set_1_sensor.values()))
data_nulmeting = np.array(list(data_nulmeting.values()))

# Each 1st row is the voltage, each 2nd row is the time
# Each third row is the standard deviation

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

OD_values = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 2, 3, 4])
OD_values_hoog = np.array([2, 3, 4])

OD_values = OD_values

# Each voltage set is coupled to an OD value
avg_nulmeting = np.average(np.array([np.average(voltages_nulmeting[i]) for i in range(voltages_nulmeting.shape[0])]))


# Calculate the OD values
transmission_set1 = np.abs(avg_voltage_set12 / avg_nulmeting)

OD_set1 = -np.log10(transmission_set1)
print(OD_set1)

pl31 = Default(OD_values[:7], OD_set1[:7], y_err=std[:7], data_label="ML8511 UV versterkt", colour="g", fx=fit_func, linestyle="",
              x_label="OD filter waarde", y_label="OD gemeten waarde", func_format="fit lin. gebied: y = {0}x",
              legend_loc="lower right", capsize=5, decimal_comma=False, add_mode=True)
pl32 = Default(OD_values[7:], OD_set1[7:], y_err=std[7:], colour="g", linestyle="",
              add_mode=True, data_label="", capsize=5)

# pl1.save_as = "ODOD_versterkt.png"
pl1 += pl31
pl1 += pl32
pl1()

# plt.savefig("data_thorlas/plot_ODOD.png", dpi=600)
