import random

import numpy as np

from trajectory_toolkit.selectors.SelectorInterface import SelectorInterface


class Random(SelectorInterface):

    def __init__(self, normalizer, movelets_per_class=10, verbose=True):
        self.verbose = verbose
        self.n_movelets = movelets_per_class
        self.normalizer = normalizer

    def fit(self, X):
        return self

    """
    l'output sarà:
    tid, class, time, c1, c2, geohash
    """

    def transform(self, tid: np.ndarray, classes: np.ndarray, time: np.ndarray, X: np.ndarray, partid: np.ndarray):
        selected = []
        pk_array = np.array(list(zip(tid, partid)))

        for classe in np.unique(classes):
            to_choice = np.unique(pk_array[classes == classe], axis=0).tolist()

            choices = random.sample(to_choice, self.n_movelets)
            selected.append(choices)

        selected = [el for lista in selected for el in lista]

        to_keep_indeces = np.isin(pk_array, selected).all(axis=1)

        return tid[to_keep_indeces], classes[to_keep_indeces], time[to_keep_indeces], X[to_keep_indeces], \
               partid[to_keep_indeces]
