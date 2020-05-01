import numpy as np
import numpy.matlib
import hdbscan
from beer_app.data.data_matrix import Data_Matrix


class Rec_Engine:

    def __init__(self, user_data):
        self.user_data = user_data
        self.data = Data_Matrix()
        self.distance_matrix = self.data.distance_matrix()
        self.kw_matrix,
        self.num_clusters = self.master_kw_matrix()
        self.medoid_vectors = self.medoid_vectors()
        self.affinity_vector = self.affinity_vector()

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
            
            # take user data and determine the distance to medoids - Test Distance Matrix

            # element wise multiplication of Test Distance Matrix and Recency Weighting
            
            # return self.affinity_vector

        # Affinity is a measure of similarity, therefore we want to find the similarity between
        # the items consumed and the precalculated genre/cluster medoids. Recency weighting is
        # applied to transaction history, giving recent history the greatest emphasis

        def affinity_vector(self):
            
            # num_days = len(self.user_da)
            
            # Find distances from user_data to precomputed cluster medoids
            user_distance_matrix = np.zeros((self.num_clusters, num_days))
            
            for idx_1 in range(self.num_clusters):
                for idx_2 in range(num_days):
                    user_distance_matrix[idx_1,idx_2] = \
                    self.pairwise_distance\
                    (self.user_data[idx_2,:],self.medoid_vectors[idx_1,:])
                    
            # Normalize so that all distances are between 0 and 1
            user_distance_matrix = user_distance_matrix/(np.amax(user_distance_matrix))
            
            # Convert to affinity matrix
            user_affinity_matrix = 1 - user_distance_matrix
            
            # Impose recency weighting. If "recenceyBlock = 5", the last 5 days affinity
            # values will be given the greatest emphasis, the affinity values from the 5
            # days before will be given second greatest emphasis. The emphasis values
            # decrease exponentially.
            
            recency_block= 5
            recency_weight_factor = 0.8
            factor = 0
            weight_vector = np.zeros((1, num_days))
            
            for idx in range(num_days,0,-recency_block):
                start_idx = idx
                end_idx = max(start_idx-recency_block+1, 1)
                weight_vector[0,end_idx-1:start_idx] = recency_weight_factor**factor
                factor += 1
                
            weight_vector = np.matlib.repmat(weight_vector, self.num_clusters, 1) #duplicate vector
            user_affinity_matrix = user_affinity_matrix * weight_vector #elementwise mult
            user_affinity_matrix = np.sum(user_affinity_matrix, axis=1)
            affinity_vector = user_affinity_matrix / np.sum(user_affinity_matrix)
            
            return affinity_vector

        # Returns pairwise distance of user_data vs. medoid vectors    
        @staticmethod
        def pairwise_distance(binary_string_1, binary_string_2):
            
            if len(binary_string_1) != len(binary_string_2):
                raise Exception('Binary strings must be of equal length! \n')
            else:
                string_length = len(binary_string_1)
                
            num_mismatches = np.sum(np.logical_xor(binary_string_1, binary_string_2))
            distance = num_mismatches / string_length
            
            return distance

