import numpy as np
from sklearn.base import TransformerMixin

from trajectory_toolkit.partitioners.Geohash import Geohash

from trajectory_toolkit.normalizers.FirstPoint import FirstPoint

from trajectory_toolkit.selectors.Random import Random


class Geolet(TransformerMixin):
    def __init__(self, precision=7,
                 partitioner='Geohash',
                 normalizer='FirstPoint',
                 selector='Random', geolet_per_class = 10,
                 distance='ed',
                 verbose=False):

        self.verbose = verbose

        if partitioner == 'Geohash':
            self.partitioner = Geohash(precision=precision, verbose=verbose)

        if normalizer == 'FirstPoint':
            self.normalizer = FirstPoint()

        if selector == 'Random':
            self.selector = Random(normalizer=self.normalizer, movelets_per_class=geolet_per_class, verbose=verbose)

        self.distance = distance

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.y = y
        return self

    #specific order: tid, class, time, lat, lon
    def transform(self, X: np.ndarray):
        tid = X[:, 0]
        time = X[:, 1]
        lat_lon = X[:, 2:]
        y = self.y

        partitions = self.partitioner.transform(lat_lon)

        sel_tid, sel_y, sel_time, sel_X, el_partid = self.selector.transform(tid, y, time, lat_lon, partitions)


        pass
