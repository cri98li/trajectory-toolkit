import numpy as np


def _rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def sum(features: np.ndarray, window):
    if window is None:
        window = len(features)

    np.sum(_rolling_window(features, window))


def max(features: np.ndarray, window):
    if window is None:
        window = len(features)

    np.max(_rolling_window(features, window))


def min(features: np.ndarray, window):
    if window is None:
        window = len(features)

    np.min(_rolling_window(features, window))


def std(features: np.ndarray, window):
    if window is None:
        window = len(features)

    np.std(_rolling_window(features, window))


def cov(features: np.ndarray, window):
    if window is None:
        window = len(features)

    np.cov(_rolling_window(features, window))


def var(features: np.ndarray, window):
    if window is None:
        window = len(features)

    np.var(_rolling_window(features, window))
