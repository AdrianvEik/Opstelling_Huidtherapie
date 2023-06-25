
import matplotlib.pyplot as plt
import numpy as np

from AdrianPack.Fileread import Fileread
from AdrianPack.Aplot import Default

def fit_func(x, a):
    return a * x

def calculate_intesnity(x):
    # https://learn.sparkfun.com/tutorials/ml8511-uv-sensor-hookup-guide/all
    # Linear equation between 0 and 15mW/cm^2 and 1 and 3 V output
    return (x-1.5) * 15/2 * 3/4 + 1

folder = "230623_onzesensor/Met_versterking"

data_set_1_sensor = Fileread(folder+"/set1", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()
data_nulmeting = Fileread(folder+"/nulmeting", head=False, allow_duplicates=True, delimiter=" ", dtype=float)()

data_set_1_sensor = np.array(list(data_set_1_sensor.values()))
data_nulmeting = np.array(list(data_nulmeting.values()))
print(np.average(data_set_1_sensor[-2, :]), np.std(data_set_1_sensor[-2, :]))

pl = Default(data_set_1_sensor[-3, :], data_set_1_sensor[-2, :], data_label="ML8511 UV versterkt", colour="b", linestyle="-",
              x_label="Tijd $t$ [s]", y_label="Gemeten voltage $V$ [V]", capsize=0,
              legend_loc="lower right", save_as="rawdata_OD40_versterkt.png", marker="", decimal_comma=False)
pl()