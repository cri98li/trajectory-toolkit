import numpy as np
from geopy import distance


def speed(lat: np.ndarray, lon: np.ndarray, time: np.ndarray):
    d_time = time[1:] - time[:-1]
    dist_lat = lat[1:] - lat[:-1]
    dist_lon = lon[1:] - lon[:-1]
    dist = (dist_lat ** 2 + dist_lon ** 2) ** .5

    return np.append([.0], dist / d_time)


def acceleration(lat: np.ndarray, lon: np.ndarray, time: np.ndarray):
    d_time = time[1:] - time[:-1]
    dist_lat = lat[1:] - lat[:-1]
    dist_lon = lon[1:] - lon[:-1]
    dist = (dist_lat ** 2 + dist_lon ** 2) ** .5

    return np.append([.0], dist / (d_time ** 2))


def acceleration2(lat: np.ndarray, lon: np.ndarray, time: np.ndarray):
    d_time = time[1:] - time[:-1]
    dist_lat = lat[1:] - lat[:-1]
    dist_lon = lon[1:] - lon[:-1]
    dist = (dist_lat ** 2 + dist_lon ** 2) ** .5
    acc = np.append([.0], dist / (d_time ** 2))

    return np.append([.0], acc[1:] - acc[:-1])


def direction(lat: np.ndarray, lon: np.ndarray):
    dist_lat = lat[1:] - lat[:-1]
    dist_lon = lon[1:] - lon[:-1]

    return np.append([.0], np.arctan2(dist_lat, dist_lon))


def distance(lat: np.ndarray, lon: np.ndarray, ellipsoid="WGS-84"):
    returnValue = np.zeros(len(lat) - 1)
    for i in range(len(lat) - 1):
        returnValue[i] = distance.geodesic((lat[i], lon[i]), (lat[i + 1], lon[i + 1]), ellipsoid=ellipsoid).meters

    return np.append([.0], returnValue)


lat = np.array([1, 2, 2])
lon = np.array([1, 2, 4])
time = np.array([1, 2, 4])

print(speed(lat, lon, time))
print(acceleration(lat, lon, time))
print(acceleration2(lat, lon, time))
print(direction(lat, lon))
