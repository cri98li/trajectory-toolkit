import numpy as np
from sklearn.base import TransformerMixin

from trajectory_toolkit.partitioners.Geohash import Geohash

from trajectory_toolkit.normalizers.FirstPoint import FirstPoint

from trajectory_toolkit.selectors.Random import Random
from trajectory_toolkit.selectors.RandomInformationGain import RandomInformationGain

from trajectory_toolkit.distancers.Euclidean import Euclidean_distancer
from trajectory_toolkit.distancers.InterpolatedRouteDistance import InterpolatedRootDistance


class Geolet(TransformerMixin):
    def __init__(self, precision=7,
                 partitioner='Geohash',
                 normalizer='FirstPoint',
                 selector='Random', geolet_per_class=10, bestFittingMeasure=lambda x: x, top_k=3,
                                    trajectory_for_stats=100, n_neighbors=3,
                 distance='E',
                 n_jobs=1,
                 random_state=42,
                 verbose=False):

        self.verbose = verbose

        if partitioner == 'Geohash':
            self.partitioner = Geohash(precision=precision, verbose=verbose)

        if normalizer == 'FirstPoint':
            self.normalizer = FirstPoint()

        if selector == 'Random':
            self.selector = Random(normalizer=self.normalizer, n_geolet_per_class=top_k, verbose=verbose)
        elif selector == 'MutualInformation':
            self.selector = RandomInformationGain(normalizer=self.normalizer, bestFittingMeasure=bestFittingMeasure,
                                                  top_k=top_k, n_geolet_per_class=geolet_per_class,
                                                  estimation_trajectories_per_class=trajectory_for_stats,
                                                  n_neighbors=n_neighbors, n_jobs=n_jobs, random_state=random_state,
                                                  verbose=verbose)
        if distance == 'E':
            self.distancer = Euclidean_distancer(normalizer=self.normalizer, n_jobs=n_jobs, verbose=verbose)
        elif distance == 'IRP':
            self.distancer = InterpolatedRootDistance(normalizer=self.normalizer, n_jobs=n_jobs, verbose=verbose)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.y = y
        return self

    # specific order: tid, class, time, lat, lon
    def transform(self, X: np.ndarray):
        tid = X[:, 0]
        time = X[:, 1]
        lat_lon = X[:, 2:]
        y = self.y

        partitions = self.partitioner.transform(lat_lon)

        sel_tid, sel_y, sel_time, sel_X = self.selector.transform(tid, y, time, lat_lon, partitions)

        self.distancer.transform(tid, time, lat_lon, sel_tid, sel_time, sel_X)

        pass
