from sklearn.cluster import DBSCAN
import numpy as np


class ObjectClustering:

    def __init__(self, eps=0.5, min_samples=1):
        self.clustering = DBSCAN(eps=eps, min_samples=min_samples)

    def get_clusters(self, cameras: list[int], pixels: list[tuple[float, float]], points: list[tuple[float, float]]) \
            -> dict:
        if len(points) == 0:
            return {}
        clasters = self.clustering.fit(points)
        result = {}
        for index, label in enumerate(clasters.labels_):
            if result.get(label) is None:
                result[label] = {'points': [], 'cameras': {}}
            camera = cameras[index]
            coordinate = pixels[index]
            result[label]['cameras'][camera] = coordinate
            result[label]['points'].append(points[index])

        for cluster in result:
            result[cluster]['points'] = np.array(result[cluster]['points'])
            result[cluster]['mean'] = result[cluster]['points'].mean(axis=0)
        return result
