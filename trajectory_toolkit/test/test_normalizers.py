import unittest
import random

import numpy as np

from trajectory_toolkit.normalizers.FirstPoint_normalizer import FirstPoint_normalizer

class TestAlgorithms(unittest.TestCase):
    def test_firstpoint_normalizer(self):
        norm = FirstPoint_normalizer()
        X = np.array([
            ["ciao", 1, 2],
            ["ciao", 2, 2],
            ["addio", 7, 2],
        ], dtype='O')

        X_expected = np.array([
            ["ciao", 0, 0],
            ["ciao", 1, 0],
            ["addio", 0, 0]
        ], dtype='O')

        self.assertTrue(np.all(X_expected == norm.transform(X)))


if __name__ == "__main__":
    unittest.main()
