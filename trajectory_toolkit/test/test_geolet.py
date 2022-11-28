import unittest
import pandas as pd
from sklearn.model_selection import train_test_split

from trajectory_toolkit.geolet.Geolet import Geolet

class TestAlgorithms(unittest.TestCase):
    def test_geolet_animals(self):
        df = pd.read_csv("datasets/animals.zip").sort_values(by=["tid", "t"])
        df = df[["tid", "class", "t", "c1", "c2"]]

        tid_train, tid_test, _, _ = train_test_split(df.groupby(by=["tid"]).max().reset_index()["tid"],
                                                     df.groupby(by=["tid"]).max().reset_index()["class"],
                                                     test_size=.3,
                                                     stratify=df.groupby(by=["tid"]).max().reset_index()["class"],
                                                     random_state=3)

        transform = Geolet(precision=10, geolet_per_class=10)

        X = df.drop(columns="class").values
        y = df.values[:, 1]

        transform.fit_transform(X, y)





if __name__ == "__main__":
    unittest.main()
