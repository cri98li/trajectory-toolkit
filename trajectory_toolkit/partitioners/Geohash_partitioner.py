from geolib import geohash
from sklearn.exceptions import *
from tqdm.auto import tqdm
import numpy as np

from trajectory_toolkit.partitioners.PartitionerInterface import PartitionerInterface


class Geohash_partitioner(PartitionerInterface):
    """
    precision : number, default=7
    A value used by the partitioner to set the partitions size
    """

    def _checkFormat(self, X):
        if X.shape[1] != 2:
            raise DataDimensionalityWarning("The input data must be in this form [[latitude, longitude]]")
        # Altri controlli?

    def __init__(self, precision=7, verbose=True):
        self.precision = precision
        self.verbose = verbose
    """
    Controllo il formato dei dati, l'ordine deve essere: 
    tid, class, time, c1, c2
    """

    def fit(self, X):
        self._checkFormat(X)

        return self

    """
    l'output sarà una lista di encodings della forma (X.shape[0], 1)
    """

    def transform(self, X: np.ndarray):
        self._checkFormat(X)
        encodes = np.chararray((X.shape[0], 1), itemsize=self.precision)

        if self.verbose: print(F"Encoding {X.shape[0]} points with precision {self.precision}", flush=True)


        for i, row in enumerate(tqdm(X, disable=not self.verbose, position=0, leave=True)):
            encodes[i] = geohash.encode(row[0], row[1], self.precision)

        return encodes
