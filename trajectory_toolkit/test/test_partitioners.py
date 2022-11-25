import unittest
import random

import numpy as np

from trajectory_toolkit.partitioners.Geohash_partitioner import Geohash_partitioner

class TestAlgorithms(unittest.TestCase):
    def test_geohash_partitioner(self):
        array = np.array([
            [28.6132, 77.2291]
        ])

        part = Geohash_partitioner(precision=7)

        self.assertTrue(np.all(part.transform(array).flatten() == np.array([b"ttnfv2u", b"ttnfv2u", b"ttnfv2u"])))



if __name__ == "__main__":
    unittest.main()
