
import types
import time

import numpy.random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from scipy.optimize import curve_fit
from typing import Sized, Iterable, Union, Optional, Any, Type, Tuple, List, \
    Dict, Callable
from inspect import signature

try:
    from TN_code.plotten.TISTNplot import TNFormatter
except ImportError:
    try:
        from .TN_code.plotten.TISTNplot import TNFormatter
    except ImportError:
        TNFormatter = False

try:
    from Helper import test_inp, compress_ind
except ImportError:
    from .Helper import test_inp, compress_ind

# Aplot revision

class Line:
    """
    Line class object to store, compute graph lines.

    Attrs:
    :param: x,
        ObjectType -> Union[list, numpy.ndarry]
                Array with values that correspond to the input values or control
                 values.
    :param: y
        ObjectType -> Union[list, numpy.ndarry, Callable]
            Array (or function) with values that correspond to the output values f(x) or
             response values. If function, the y-array will be initialised as:
                self.y = self.y(self.x)
    :param: xerr
        ObjectType -> Union[list, numpy.ndarry, Callable]
            Array (or function) with values that correspond to the error input
             values or control values. If function, the xerr-array
             will be initialised as:
                self.xerr = self.xerr(self.x)
    :param: yerr
        ObjectType -> Union[list, numpy.ndarry, Callable]
            Array (or function) with values that correspond to the error in the
             output values f(x) or response values. If function, the xerr-array
             will be initialised as:
                self.yerr = self.yerr(self.y)

    """
    def __init__(self, x: Union[list, numpy.ndarry] = np.array([]),
                 y: Union[list, numpy.ndarry, Callable] = np.array([]),
                 xerr=np.array([]), yerr=np.array([])):

        # x => array, empty array
        self.x = x

        self.y = y

        self.xerr = xerr

        self.yerr = yerr

    def __repr__(self):
        pass

    def fit(self):
        pass

    def floating_point_average(self):
        pass


















