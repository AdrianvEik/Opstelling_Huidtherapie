
import numpy as np

def compute_OD_from_T(T):
    return -np.log10(T/100)

print(compute_OD_from_T( np.array([81, 65, 56, 45, 38 ,30,10, 0.76, 0.1, 0.001])))