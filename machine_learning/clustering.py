import pickle
from sklearn.cluster import KMeans

__author__ = 'ava-katushka'
from features_extraction.CellFeatureExtractor import CellFeatureExtractor
class ClusterBuilder:
    allSet = CellFeatureExtractor.allFeatures()
    X = allSet["X"]
    y = allSet["y"]

    @classmethod
    def kMeans(cls, n_clusters):
        model = KMeans(n_clusters=n_clusters)
        results = model.fit_predict(cls.X)
        return results


if __name__ == "__main__":
    results = ClusterBuilder.kMeans()
    print results[0]

