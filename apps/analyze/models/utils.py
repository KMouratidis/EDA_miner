"""
This module collects utility functions and models.

Functions:
    - baseline: Calculate the baseline for a time series.

Notes to others:
    Feel free to add or modify stuff here.
"""

import pandas as pd
import numpy as np
import peakutils


def _moving_average(values, roll_window=3, correction=False):
    values = pd.Series(values)
    roll = values.rolling(roll_window).mean()
    roll[:roll_window] = values[:roll_window].mean()

    if correction:
        correction = int(roll_window / 2)
        roll = roll.shift(-correction)
        roll[correction:] = values[correction:]

    return roll


def _exp_moving_average(values, window):
    weights = np.exp(np.linspace(-1., 0.5, window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]

    return a


def _ema_baseline(values, func, ema_window=7, roll_window=7):
    ema = _exp_moving_average(values, ema_window)

    roll = _moving_average(func([values, ema], axis=0), roll_window)
    roll = pd.Series(func([values, roll], axis=0))

    return roll


def baseline(values, min_max="min", deg=7, ema_window=7, roll_window=7,
             max_it=200, tol=1e-4):
    """

    Args:
        values (iterable(int)):
        min_max (str): Whether to calculate an upper or lower baseline.
        deg (int): The degree of the polynomial fitting.
        ema_window (int): Window for the exponential moving average.
        roll_window (int): Window for the simple moving average.
        max_it (int): Number of iterations for `peakutils.baseline`.
        tol (float): Least amount of change before termination of fitting \
                     in `peakutils.baseline`.

    Returns:

    """

    if min_max == "min":
        bound = np.min
    elif min_max == "max":
        bound = np.max
    else:
        raise NotImplementedError

    ema_baseline = _ema_baseline(values, bound, ema_window, roll_window)
    peakutils_baseline = peakutils.baseline(values, deg=deg,
                                            max_it=max_it,
                                            tol=tol)

    # Give double the weight to peakutil's values
    return np.mean([peakutils_baseline * 4/3,
                    ema_baseline * 2/3], 0)

