from concurrent.futures import ProcessPoolExecutor
import math
from math import sqrt

import numpy as np
import pandas as pd
from tqdm.autonotebook import tqdm

from cri98tj.distancers.DistancerInterface import DistancerInterface
from cri98tj.normalizers.NormalizerInterface import NormalizerInterface
from cri98tj.normalizers.normalizer_utils import dataframe_pivot


class DTW_distancer(DistancerInterface):

    def __init__(self, normalizer, window=1, n_jobs=1, spatioTemporalColumns=["c1", "c2"], verbose=True):
        self.verbose = verbose
        self.normalizer = normalizer
        self.spatioTemporalColumns = spatioTemporalColumns
        self.n_jobs = n_jobs
        self.window = window

    def fit(self, trajectories_movelets):
        return self

    # trajectories = tid, class, time, c1, c2
    # restituisce nparray con pos0= cluster e poi
    def transform(self, trajectories_movelets):
        trajectories, movelets = trajectories_movelets

        trajectories_df = pd.DataFrame(trajectories, columns=["tid", "class"]+self.spatioTemporalColumns)
        trajectories_df["partId"] = trajectories_df.tid
        df_pivot = dataframe_pivot(df=trajectories_df, maxLen=None, verbose=self.verbose, fillna_value=None, columns=self.spatioTemporalColumns)

        distances = np.zeros((df_pivot.shape[0], len(movelets)))

        executor = ProcessPoolExecutor(max_workers=self.n_jobs)

        ndarray_pivot = df_pivot[[x for x in df_pivot.columns if x != "class"]].values
        processes = []
        for i, movelet in enumerate(tqdm(movelets, disable=not self.verbose, position=0)):
            processes.append(executor.submit(self._foo, i, movelet, ndarray_pivot, self.spatioTemporalColumns))

        if self.verbose: print(f"Collecting distances from {len(processes)}")
        for i, process in enumerate(tqdm(processes)):
            col = process.result()
            for j, val in enumerate(col):
                distances[j, i] = val

        executor.shutdown(wait=True)
        """for i, movelet in enumerate(tqdm(movelets, disable=not self.verbose, position=0)):
            for j, val in enumerate(self._foo(i, movelet, ndarray_pivot)):
                distances[j, i] = val"""

        return np.hstack((df_pivot[["class"]].values, distances))

    def _foo(self,i, movelet, ndarray_pivot, spatioTemporalColumns):
        distances = []
        for j, trajectory in enumerate( tqdm(ndarray_pivot, disable=True, position=i+1, leave=True)):
            best_i, best_score = DTWBestFitting(trajectory=trajectory, movelet=movelet,
                                                      spatioTemporalColumns=spatioTemporalColumns,
                                                normalizer=self.normalizer, window=self.window)
            distances.append(best_score)

        return distances


def DTWBestFitting(trajectory, movelet, spatioTemporalColumns, window=5, normalizer=NormalizerInterface()):  # nan == end
    if len(trajectory) % len(spatioTemporalColumns) != 0:
        raise Exception(f"la lunghezza della traiettoria deve essere divisivile per {len(spatioTemporalColumns)}")
    if len(movelet) % len(spatioTemporalColumns) != 0:
        raise Exception(f"la lunghezza della traiettoria deve essere divisivile per {len(spatioTemporalColumns)}")

    offset_trajectory = int(len(trajectory) / len(spatioTemporalColumns))
    offset_movelet = int(len(movelet) / len(spatioTemporalColumns))

    len_mov = 0
    for el in movelet:
        if np.isnan(el) or len_mov >= offset_movelet:
            break
        len_mov += 1

    len_t = 0
    for el in trajectory:
        if np.isnan(el) or len_t >= offset_trajectory:
            break
        len_t += 1

    if len_mov > len_t:
        return DTWBestFitting(movelet, trajectory, spatioTemporalColumns, window, normalizer)

    trajectory_dict = [None for x in spatioTemporalColumns]
    movelet_dict = [None for x in spatioTemporalColumns]

    for i, col in enumerate(spatioTemporalColumns):
        trajectory_dict[i] = normalizer._transformSingleTraj(trajectory[i * offset_trajectory:(i * offset_trajectory) + len_t])
        movelet_dict[i] = normalizer._transformSingleTraj(movelet[i * offset_movelet:(i * offset_movelet) + len_mov])


    bestScore = math.inf
    best_i = -1
    for i in range(max(len_t - len_mov - window, 0) + 1):
        trajectory_dict_cut = dict()
        for j, col in enumerate(spatioTemporalColumns):
            trajectory_dict_cut[j] = normalizer._transformSingleTraj(trajectory_dict[j][i:i + len_mov + window])
        returned = _DTWBestFitting(trajectory_dict_cut, movelet_dict, spatioTemporalColumns)
        if returned is not None and returned < bestScore:
            bestScore = returned
            best_i = i

    return best_i, bestScore

def _dist(c1_a, c2_a, c1_b, c2_b):
    return sqrt( (c1_a - c1_b)**2 + (c2_a-c2_b)**2 )

def _DTWBestFitting(trajectory, movelet, spatioTemporalColumns):
    spatioTemporalColumns = [x for x in spatioTemporalColumns if x not in ["t", "time", "timestamp", "TIMESTAMP"]]

    n, m = len(movelet[0]), len(trajectory[0])
    matrix = [[(None, None) for _ in range(m + 1)] for _ in range(n + 1)]  # (n, value)

    matrix[0][0] = (0, 0)
    matrix[0][1:] = [(1, float("inf")) for _ in matrix[0][1:]]
    for row in matrix[1:]:
        row[0] = (1, float("inf"))

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            n_min, val_min = sorted([matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1]], key=lambda x: 0 if x[0] == 0 else x[1] / x[0])[0]

            d = _dist(movelet[0][i - 1], movelet[1][i - 1], trajectory[0][j - 1], trajectory[1][j - 1])

            matrix[i][j] = (n_min + 1, d + val_min)

    return matrix[-1][-1][1] / matrix[-1][-1][0]


"""def _DTWBestFitting(trajectory, movelet, spatioTemporalColumns, window=None):
    spatioTemporalColumns = [x for x in spatioTemporalColumns if x not in ["t", "time", "timestamp", "TIMESTAMP"]]

    n, m = len(movelet[0]), len(trajectory[0])
    dtw_matrix = np.zeros((n + 1, m + 1))
    for i in range(n + 1):
        for j in range(m + 1):
            dtw_matrix[i, j] = np.inf
    dtw_matrix[0, 0] = 0

    for i in range(1, n + 1):
        loop_min =1
        loop_max = m
        if window is not None:
            loop_min = max(1, i-window)
            loop_max = min(m, i+window)

        for j in range(loop_min, loop_max + 1):
            cost = 0
            for k in range(len(spatioTemporalColumns)):
                cost += (movelet[k][i - 1] - trajectory[k][j - 1]) ** 2
            cost **= (1 / len(spatioTemporalColumns))
            # take last min from a square box
            last_min = np.min([dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]])
            dtw_matrix[i, j] = cost + last_min
    return dtw_matrix[n, m]
"""
