import numpy as np
from sklearn.exceptions import DataDimensionalityWarning
from tqdm.auto import tqdm

from trajectory_toolkit.normalizers.NormalizerInterface import NormalizerInterface

class FirstPoint_normalizer(NormalizerInterface):
    def _checkFormat(self, X):
        if X.shape[1] != 3:
            raise DataDimensionalityWarning(
                "The input data must be in this form [[part, latitude, longitude]]")

    def __init__(self, fillna=None, verbose=True):
        self.verbose = verbose
        self.fillna = fillna

    def fit(self, X):
        self._checkFormat(X)

        return self

    """
    l'input sarà:
    partId, latitude, longitude
    """

    def transform(self, X: np.ndarray):
        X_res = X.copy()

        first = (None, None, None)
        for row in tqdm(X_res, disable=not self.verbose, position=0, leave=True):
            if first[0] != row[0]:
                first = row.copy()

            row[1:] -= first[1:]

        return X_res

    def _transformSingleTraj(self, X):  # X è una lista di numeri semplici TODO: CHECK
        row = X.copy()

        return list(map(lambda x: x - row[0], row))
