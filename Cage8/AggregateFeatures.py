import numpy as np
import scipy
def interpolate(val1, time1, val2, time2, time):
    interp = scipy.interpolate.interp1d([time1, time2], [val1, val2])

    return interp(time)


#window_type= None-> #features; 'time'-> time based; 'distance'-> distance based
def _rolling_window(a, window, window_type, time=None, distance=None):
    if window_type is None:
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        for row in np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides):
            yield row
    elif window_type == 'time': #TODO: optimize
        if time is None:
            raise ValueError( f"time cannot be None when window_type={window_type}")
        for i in range(len(time-1)):
            total_time = 0
            values = []

            for j, corr, succ in enumerate(zip(time[i:-1], time[i+1:])):
                delta = succ - corr
                if total_time + delta > window:
                    interpolated_value = interpolate(features[i+j], corr, features[i+j+1], succ, window)
                    values.append(interpolated_value)
                    break
                else:
                    total_time += delta
                    values.append(features[i+j])
            yield values
    elif window_type == 'distance': #TODO: optimize
        if distance is None:
            raise ValueError(f"distance cannot be None when window_type={window_type}")
        for i in range(len(distance - 1)):
            total_distance = 0
            values = []

            for j, corr, succ in enumerate(zip(distance[i:-1], distance[i + 1:])):
                delta = succ - corr
                if total_distance + delta > window:
                    interpolated_value = interpolate(features[i + j], corr, features[i + j + 1], succ, window)
                    values.append(interpolated_value)
                    break
                else:
                    total_distance += delta
                    values.append(features[i + j])
            yield values
    else:
        raise ValueError(f"window_type={window_type} unsupported. window_type must be in [None, 'time', 'distance']")


def sum(features: np.ndarray, window, window_type = None, time=None, distance=None):
    if window is None:
        window = len(features)

    #np.sum(_rolling_window(features, window, window_type))

    return np.sum(np.fromiter(_rolling_window(features, window, window_type, time, distance), dtype=np.dtype((float, 3))), axis=1)


def max(features: np.ndarray, window, window_type = None, time=None, distance=None):
    if window is None:
        window = len(features)

    return np.max(np.fromiter(_rolling_window(features, window, window_type, time, distance), dtype=np.dtype((float, 3))), axis=1)


def min(features: np.ndarray, window, window_type = None, time=None, distance=None):
    if window is None:
        window = len(features)

    return np.min(np.fromiter(_rolling_window(features, window, window_type, time, distance), dtype=np.dtype((float, 3))), axis=1)


def std(features: np.ndarray, window, window_type = None, time=None, distance=None):
    if window is None:
        window = len(features)

    return np.std(np.fromiter(_rolling_window(features, window, window_type, time, distance), dtype=np.dtype((float, 3))), axis=1)

def cov(features: np.ndarray, window, window_type = None, time=None, distance=None):
    if window is None:
        window = len(features)

    return np.cov(np.fromiter(_rolling_window(features, window, window_type, time, distance), dtype=np.dtype((float, 3))), axis=1)

def var(features: np.ndarray, window, window_type = None, time=None, distance=None):
    if window is None:
        window = len(features)

    return np.var(np.fromiter(_rolling_window(features, window, window_type, time, distance), dtype=np.dtype((float, 3))), axis=1)

def rate_upper(features: np.ndarray, threshold, window, distance=None, time=None, window_type = None):
    if window is None:
        window = len(features)

    returnValue = np.zeros(len(features) - window + 1)

    """count = 0
    for i in range(len(features)):

        if features[i] > threshold:
            count += 1
        if i - window + 1 > 0 and features[i - window] > threshold:
            count -= 1
        if i - window + 1 >= 0:
            returnValue[i - window + 1] = count"""

    for i, window_value in enumerate(_rolling_window(features, window, window_type, time, distance)):
        for el in window_value:
            if el > threshold:
                returnValue[i] += 1

    if distance is not None:
        returnValue /= distance

    return returnValue


def rate_below(features: np.ndarray, threshold, window, distance=None, time=None, window_type = None):
    return rate_upper(features=features, threshold=threshold * -1, window=window, window_type=window_type,
                      distance=distance, time=time)


features = np.array([1,1,1,2,3,2,2,3,6,7])

res = sum(features, 3)

print(f"result({type(res)}): {res}")