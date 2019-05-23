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
from scipy import sparse
from scipy.sparse.linalg import spsolve


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


# https://stackoverflow.com/a/50160920/6655150
def _als_baseline(values, lam=10, p=0.002, niter=10):
    L = len(values)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L-2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w*values)
        w = p * (values > z) + (1-p) * (values < z)
    return z


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
        np.array: the baseline.
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
    return (2/3 * np.mean([peakutils_baseline * 4/3,
                    ema_baseline * 2/3], 0)
            + 1/3 * _als_baseline(values))

