import math
import random

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier

import Cage8.BasicFeatures as bf
import Cage8.AggregateFeatures as af


class T_CIF(BaseEstimator, ClassifierMixin):
    def __init__(self, n_trees, n_interval, min_length, seed=42):
        self.clf = None
        self.intervals = []
        self.n_trees = n_trees
        self.n_interval = n_interval
        self.min_length = min_length
        self.seed = seed

    def generate_intervals(self, max_len):
        random.seed(self.seed)

        starting_p = random.sample(range(0, max_len-self.min_length), self.n_interval)
        ending_p = []
        for p in starting_p:
            l = random.randint(self.min_length, max_len-p)+p

            ending_p.append(l)

        return starting_p, ending_p

    def _transform(self, X, starts, stops):
        features = []

        for (X_lat, X_lon, X_time) in X:
            feature = []
            for start, stop in zip(starts, stops):
                feature.append(af.max(bf.speed(X_lat[start:stop], X_lon[start:stop], X_time[start:stop]), None))
            features.append(feature)

        return np.array(features)[:,:,0]

    def fit(self, X, y):
        min_l = min([len(x[0]) for x in X])

        self.starts, self.stops = self.generate_intervals(min_l)

        self.clf = RandomForestClassifier(n_estimators=self.n_trees, max_depth=2)

        self.clf.fit(self._transform(X, self.starts, self.stops), y)

        return self

    def predict(self, X):
        return self.clf.predict(self._transform(X, self.starts, self.stops))



