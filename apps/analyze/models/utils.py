import pandas as pd
import numpy as np


def baseline(values, min_max="min", ema_window=7, roll_window=7):
    """ Numpy implementation of EMA
    """

    if min_max == "min":
        bound = np.min
    elif min_max == "max":
        bound = np.max
    else:
        raise NotImplementedError

    weights = np.exp(np.linspace(-1., 0., ema_window))
    weights /= weights.sum()
    ema =  np.convolve(values, weights, mode='full')[:len(values)]
    ema[:ema_window] = ema[ema_window]

    roll = pd.Series(bound([values, ema],axis=0))
    roll = roll.rolling(roll_window).mean()
    roll[:roll_window] = bound(values[:roll_window])
    roll = pd.Series(bound([values, ema],axis=0))

    return roll
