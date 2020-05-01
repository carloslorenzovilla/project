import numpy as np
import numpy.matlib
import hdbscan
from beer_app.data.data_matrix import Data_Matrix


class Rec_Engine:

    def __init__(self, user_data):
        self.user_data = user_data
        self.data = Data_Matrix()
        self.distance_matrix = distance_matrix()
        self.kw_matrix, 
        self.num_clusters = master_kw_matrix()
        self.medoid_vectors = medoid_vectors()
        self.affinity_vector = affinity_vector()

    def master_kw_matrix(self):

            # calculate the distances
            clusters = hdbscan.HDBSCAN(metric='precomputed')
            clusters.fit(self.distance_matrix)

            # attach labels
            for idx, label in enumerate(clusters.labels_):
                kw_matrix[idx, 0] = label
            # sort by cluster
            kw_matrix = kw_matrix[np.argsort(kw_matrix[:, 0])]

            num_clusters = max(clusters.labels_ + 1)

        return kw_matrix, num_clusters

    # Calculate medoids of each cluster/genre, that is the item whose average distance
    # to all other items within a cluster is smallest. Returns array of corresponding
    # item indeces.
    def medoid_vector(self):

        cluster_assignments = [
                                                list(np.where(self.kw_matrix[:, 1] == index)[0])
                                                for index
                                                in range(self.num_clusters)
                                             ]

        # medoids are meaningful only in the number of elements > 2
        medoid_list = np.zeros(self.num_clusters)

        for cidx in range(self.num_clusters):

            # find elements in current cluster
            elements_in_cluster = cluster_assignments[cidx]
            num_elements_in_cluster = len(elements_in_cluster)

            if num_elements_in_cluster == 1:
                medoid_list[cidx] = elements_in_cluster[0]
            elif num_elements_in_cluster == 2:
                medoid_list[cidx] = elements_in_cluster[0]
            else:
                avg_dist_vector = np.zeros(num_elements_in_cluster)

                for nidx in range(num_elements_in_cluster):
                    current_point = elements_in_cluster[nidx]
                    other_points = np.setdiff1d(
                        elements_in_cluster, current_point)
                    avg_dist_vector[nidx] = \
                        np.mean(distance_matrix[current_point, other_points])

                min_dist_idx = list(
                    np.where(avg_dist_vector == np.min(avg_dist_vector))[0])
                min_dist_idx = min_dist_idx[0]
                medoid_list[cidx] = elements_in_cluster[min_dist_idx]

            medoid_vectors = self.kw_matrix[medoid_list.astype(int), 2:]

        return medoid_vectors

        def affinity_vector(self):
            
            # self.user_data
            # self.medoid_vectors
            
            # take user data and determine the distance to medoids
            
            # return self.affinity_vector


