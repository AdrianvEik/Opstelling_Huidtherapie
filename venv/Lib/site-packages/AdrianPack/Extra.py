""""
Collection of helper functions

- DMM_ERR: Error in DMM (currently only DC  voltage)
- Peak_finder: Find peaks in weird Data sets.
-

DEPENDENCIES:
    numpy, pandas, matplotlib and *TISTNplot.
*optional
"""

import numpy as np
from typing import Iterable, Tuple, Union, Iterator
try:
    from Helper import compress_ind, compress_width, test_inp
except ImportError:
    from .Helper import compress_ind, compress_width, test_inp

def calc_err_DMM(unit: str, val: float, freq=1.0) -> Iterable:
    """
    unit in "(factor) (volt/amp)"
    val, value in SI.
    e_type "DC"/"AC"
    freq frequency in Hertz
    """
    unit = unit.lower()
    # Standard input is DC
    assert (lambda u: u.split(' ')[2] if len(u.split(' ')) == 3 else 'dc')(unit)\
           in ['ac', 'dc']
    # Assert the inputs are correct
    assert (lambda u: u.split(' ')[1] if 2 <= len(u.split(' ')) <= 3 else u.split(' ')[0])(unit)\
           in ['volt', 'ampere']
    assert (lambda u: u.split(' ')[0] if 2 <= len(u.split(' ')) <= 3 else 'None')(unit)\
           in ['nano', 'micro', 'milli', 'None', 'kilo', 'mega']

    factor_val = (lambda u: u.split(' ')[0] if len(u.split(' ')) == 2 else 'None')(unit)
    unit = (lambda u: u.split(' ')[1] if len(u.split(' ')) == 2 else u.split(' ')[0])(unit)
    e_type = (lambda u: u.split(' ')[2] if len(u.split(' ')) == 3 else 'dc')(unit)

    factor = {
        'nano': 10e-9,
        'micro': 10e-6,
        'milli': 10e-3,
        'None': 1,
        'kilo': 10e3,
        'mega': 10e6
    }
    val = val * factor[factor_val]

    if e_type == "dc":
        if unit in 'volt':
            unit = {0.4: 4 * 10**(-5),
                    4: 4 * 10**(-4),
                    40: 4 * 10**(-3),
                    400: 4 * 10**(-2),
                    1000: 4 * 10**(-1)}
            distance = [(lambda i: i - val if i - val > 0 else float('inf'))(i)
                        for i in list(unit.keys())]
            return unit[list(unit.keys())[
                distance.index(min(distance))]] + val * 0.08 * 10 ** (-2)
        elif unit in 'ampere':
            unit = {0.4: 4 * 10**(-5),
                    4: 4 * 10**(-4),
                    40: 4 * 10**(-3),
                    400: 4 * 10**(-2),
                    1000: 4 * 10**(-1)}
            distance = [(lambda i: i - val if i - val > 0 else float('inf'))(i)
                        for i in list(unit.keys())]
            return unit[list(unit.keys())[
                distance.index(min(distance))]] + val * 0.08 * 10 ** (-2)

    elif e_type == "ac":
        if unit in 'volt':
            unit_freq = {0.4: 4 * 10**(-5),
                    4: 4 * 10**(-4),
                    40: 4 * 10**(-3),
                    400: 4 * 10**(-2)
                    }
        elif unit in 'ampere':
            return None



def trap_int(x: Iterable, y: Iterable, **kwargs) -> Iterable:
    """
    Return the trapezium integral of the area under x and y with optional
    propagation of error in either (both) x_err or (and) y_err.
    :rtype: Iterable.
    :param x:
        Array like of x values.
    :param y:
        Array like of integrand values.
    :param: x_err:
        Array like of error in x.
    :param: y_err:
        Array like of error in y.
    :return:
        Area under x, y graph
    """
    x, y = np.array(x, np.float32), np.array(y, dtype=np.float32)

    xerr = np.zeros(x.shape)
    yerr = np.zeros(y.shape)

    if "x_err" in kwargs:
        test_inp(kwargs["x_err"], (list, np.ndarray), "error in x")
        xerr = np.array(kwargs["x_err"], np.float32)

    if "y_err" in kwargs:
        test_inp(kwargs["y_err"], (list, np.ndarray), "error in y")
        yerr = np.array(kwargs["y_err"], np.float32)

    try:
        assert x.shape == y.shape == xerr.shape == yerr.shape
    except AssertionError:
        if "y_err" in kwargs and "x_err" in kwargs:
            raise IndexError(
                "Shape of x_err, y_err, x and y should be the same but"
                " are {0}, {1}, {2} and {3}".format(xerr.shape, yerr.shape,
                                                    x.shape, y.shape)
            )
        elif "x_err" in kwargs:
            raise IndexError(
                "Shape of x_err, x and y should be the same but"
                " are {0}, {1} and {2}".format(xerr.shape, x.shape, y.shape)
            )
        elif "y_err" in kwargs:
            raise IndexError(
                "Shape of y_err, x and y should be the same but"
                " are {0}, {1} and {2}".format(yerr.shape, x.shape, y.shape)
            )
        else:
            raise IndexError(
                "Shape of x and y should be the same but"
                " are {0} and {1}".format(x.shape, y.shape)
            )

    try:
        assert x.ndim == y.ndim == xerr.ndim == yerr.ndim == 1
    except AssertionError:
        raise NotImplementedError("The dimensions of all input arrays should be"
                                  "1, multi dimensional integration is not"
                                  " implemented yet")

    # Calculating the y and x parts of the integral (as given in the question)
    # xprime = x_(i-1) - x_i
    xprime = np.insert(x[1:] - x[:-1], 0, 0)
    yprime = np.insert(y[1:] + y[:-1], 0, 0) * 1/2

    # Calculating the integral xprime * yprime.
    prime = np.cumsum(xprime * yprime)

    # Calculating the attributions to error of x and y.
    # 0 + (x(i)^2 + x(i-1)^2)^(1/2)
    xprime_err = np.sqrt(np.insert(np.power(xerr[1:], 2) + np.power(xerr[:-1], 2), 0, 0))
    yprime_err = np.sqrt(np.insert(np.power(yerr[1:], 2) + np.power(yerr[:-1], 2), 0, 0)) / 2

    # Summing the error and propagating error in x and y
    # (sum(|x_i * y_i|^2 * ((errx_i / x_i)^2 * (erry_i / y_i)^2)^(1/2)))^(1/2)
    prime_err = np.sqrt(
        np.cumsum(
            np.power(np.insert(
                np.absolute(xprime[1:] * yprime[1:]) * np.sqrt(
                    np.power(np.divide(xprime_err[1:], xprime[1:]), 2) + np.power(np.divide(yprime_err[1:], yprime[1:]), 2)
                ),
                       0, 0
            ), 2)
        )
    )
    if "x_err" in kwargs or "y_err" in kwargs:
        return prime, prime_err
    else:
        return prime


def dep_trap(x, y, xerr, yerr):
    """
    Calculate the area (with error) under datapoints x, y(x) with dependent error xerr, yerr

    :param x: 1D array with datapoints x
    :param y: 1D array with datapoints y(x)
    :param xerr: 1D array with error in datapoints x
    :param yerr: 1D array with error in datapoints y(x)
    :return:[0] 1D array with cumulitive areas under datapoints y(x_i); y(x_i-1) for all datapoints in y(x)
    :return:[1] 1D array with cumulitive error in areas under datapoints y(x_i); y(x_i-1) for all datapoints in y(x)
    """
    x, y, xerr, yerr = np.array(x, np.float32), np.array(y,
                                                         dtype=np.float32), np.array(
        xerr, np.float32), np.array(yerr, dtype=np.float32)

    try:
        assert x.shape == y.shape == xerr.shape == yerr.shape
    except AssertionError:
        raise IndexError("Shape of x and y should be the same but"
                         " are {0} and {1}".format(x.shape[0], y.shape[1]))

    xprime = np.insert(x[1:] - x[:-1], 0, 0)
    yprime = np.insert(y[1:] + y[:-1], 0, 0) * 1 / 2

    opp = np.cumsum(xprime * yprime)

    xprime_err = np.sqrt(
        np.insert(np.power(xerr[1:], 2) + np.power(xerr[:-1], 2), 0, 0))
    yprime_err = np.sqrt(
        np.insert(np.power(yerr[1:], 2) + np.power(yerr[:-1], 2), 0, 0)) / 2

    # Calculating each area between y_i and y_(i-1)
    # ( 0 + ||x_i * y_i|^2 * ((errx_i / x_i)^2 * (erry_i / y_i)^2)^(1/2)| + opp_err[i-1])
    opp_err = np.cumsum(
        np.absolute(
            np.insert(
                np.absolute(xprime[1:] * yprime[1:]) * np.sqrt(
                    np.power(np.divide(xprime_err[1:], xprime[1:]),
                             2) + np.power(
                        np.divide(yprime_err[1:], yprime[1:]), 2)
                ), 0, 0
            )
        )
    )

    return opp, opp_err


def derive(x: Iterable, y: Iterable, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
    """"
    Derive data of x with respect to y
    :rtype: tuple(1D numpy array, 1D numpy array)
    :param: x
        Array like 1D for dx or delta x
    :param: y
        Array like 1D for to dy or delta y
    :return:
        Array like 1D of dy/dx and error in this value
    """
    x, y = np.array(x, np.float32), np.array(y, dtype=np.float32)

    xerr = np.zeros(x.shape)
    yerr = np.zeros(y.shape)

    if "x_err" in kwargs:
        test_inp(kwargs["x_err"], (list, np.ndarray), "error in x")
        xerr = np.array(kwargs["x_err"], np.float32)

    if "y_err" in kwargs:
        test_inp(kwargs["y_err"], (list, np.ndarray), "error in y")
        yerr = np.array(kwargs["y_err"], np.float32)

    try:
        assert x.shape == y.shape == xerr.shape == yerr.shape
    except AssertionError:
        if "y_err" in kwargs and "x_err" in kwargs:
            raise IndexError(
                "Shape of x_err, y_err, x and y should be the same but"
                " are {0}, {1}, {2} and {3}".format(xerr.shape, yerr.shape,
                                                    x.shape, y.shape)
            )
        elif "x_err" in kwargs:
            raise IndexError(
                "Shape of x_err, x and y should be the same but"
                " are {0}, {1} and {2}".format(xerr.shape, x.shape, y.shape)
            )
        elif "y_err" in kwargs:
            raise IndexError(
                "Shape of y_err, x and y should be the same but"
                " are {0}, {1} and {2}".format(yerr.shape, x.shape, y.shape)
            )
        else:
            raise IndexError(
                "Shape of x and y should be the same but"
                " are {0} and {1}".format(x.shape, y.shape)
            )

    try:
        assert x.ndim == y.ndim == xerr.ndim == yerr.ndim == 1
    except AssertionError:
        raise NotImplementedError("The dimensions of all input arrays should be"
                                  "1, multi dimensional integration is not"
                                  " implemented yet")

    dy, dx = y[1:] - y[:-1], x[1:] - x[:-1]
    dy_e = np.insert(np.sqrt(np.power(yerr[1:], 2) - np.power(yerr[:-1], 2)), 0, 0)
    dx_e = np.insert(np.sqrt(np.power(xerr[1:], 2) - np.power(xerr[:-1], 2)), 0, 0)
    dy_dx = np.insert(np.divide(dy, dx), 0, 0)
    dy, dx = np.insert(dy, 0, 0), np.insert(dx, 0, 0)
    return dy_dx, dy_dx *np.sqrt(
        np.power(np.divide(dy_e, np.absolute(dy)), 2) + np.power(np.divide(dx_e, np.absolute(dx)), 2)
    )


def compress_array(x: np.ndarray, width: Union[float, int] = 0,
                   **kwargs) -> Iterator[tuple]:
    """"
    Compress an array to have a x slice width of param width using a floating
    average.

    :rtype: 1D array
    :param: x:
        Array to be compressed to entries of width given by slice width.
        OR
        Array wherein 1 index will be with_ind indexes in the original array.
        OR
        List of arrays.
    :param: width:
        The numerical width of a slice in the compressed array, only used for
        sequential data sets.
    :param: width_ind
        The new size of x.
    :param: extra_arr
        list of arrays that should be compressed to the same (relative) width of x.
        These should be of equal lenght
    :param: use_same_width
        Bool, if set to True the other compressed arrays in x will use the exact value
        of width. Default False use when arrays in x are of unequal length.
    :return:
        Compressed array(s) in a tuple or array.
    """
    width, unequal_extra_arr = float(width), []
    compress = compress_width

    if "width_ind" in kwargs and width != 0:
        raise NotImplementedError("Both width_ind and width have values this"
                                  " is currently not implemented.")
    elif "width_ind" in kwargs:
        test_inp(kwargs["width_ind"], int, "width_ind")
        compress = compress_ind
        width = kwargs["width_ind"]

    if isinstance(x[0], np.ndarray):
        c_list, i = [], 0
        for arr in x:
            test_inp(arr, np.ndarray, "x")
            res = compress(arr, width)
            c_list.append(res[0])
            width = res[1]
            compress = compress_ind
            i += 1

    else:
        c_list = compress(x, width)

    return tuple(c_list)


# TODO: maybe add somewhere else? apart math section?
def gauss_elim(a, v) -> np.ndarray:
    """"
    Calculate the x vector using gauss elimination

    :param: a
        A array from standard form A * x = v
        number or rows must match length of v
    :param: v
        v array from standard form A * x = v
        length must match amount of rows of A
    :return: x
        :rtype: np.ndarray
        x array from standard form A * x = v
    """

    # Test input values
    try:
        assert len(v) == a.shape[0]
    except AssertionError:
        raise IndexError("Length mismatches amount of rows of A.")

    for n in range(len(v)):
        # Divide by "first" element
        first_elem = a[n, n]
        a[n, :] /= first_elem
        v[n] /= first_elem

        for i in range(n + 1, len(v)):
            # "first" element of next row is the factor the n-1 row needs
            # to be multiplied by to subtract this element to zero
            factor = a[i, n]

            a[i, :] -= factor * a[n, :]
            v[i] -= factor * v[n]

    # Initiate x array
    x = np.zeros(v.shape, dtype=float)
    for i in range(len(v)).__reversed__():
        # Work from the bottom to the top subtract previous results
        x[i] = v[i]
        for j in range(i + 1, len(v)):
            x[i] -= a[i, j] * x[j]
    return x


