
import matplotlib.pyplot as plt
import numpy as np

from AdrianPack.Fileread import Fileread

data_set_1_sensor = Fileread("data_thorlas/set1", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_set_2_sensor = Fileread("data_thorlas/set2", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()

data_set_1_sensor = np.array(list(data_set_1_sensor.values()))
data_set_2_sensor = np.array(list(data_set_2_sensor.values()))

# Each 1st row is the voltage, each 2nd row is the time
# Each third row is the standard deviation

voltages_set1 = data_set_1_sensor[0:-1:3, :]
voltages_set2 = data_set_2_sensor[0:-1:3, :]

times_set1 = data_set_1_sensor[1:-1:3, :]
times_set2 = data_set_2_sensor[1:-1:3, :]

std_set1 = data_set_1_sensor[2:-1:3, :]
std_set2 = data_set_2_sensor[2:-1:3, :]

OD_values = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1, 2, 3])

# Each voltage set is coupled to an OD value
for i in range(9):
    plt.plot(OD_values[i], np.average(voltages_set1[i]), "o", color="blue")
    plt.plot(OD_values[i], np.average(voltages_set2[i]), "o", color="red")

plt.savefig("data_thorlas/plot.png")
