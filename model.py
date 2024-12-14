import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
from mpl_toolkits.mplot3d import Axes3D

class DBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        self.eps = eps
        self.min_samples = min_samples
        self.labels_ = None  
        self.core_samples_ = None 
        self.noise_ = None 

    def fit(self, data):
        n_samples = len(data)
        self.labels_ = -1 * np.ones(n_samples) 
        dist_matrix = euclidean_distances(data)        
        core_samples = []
        clusters = []        
        cluster_id = 0  

        for i in range(n_samples):
            if self.labels_[i] != -1:  
                continue

            neighbors = np.where(dist_matrix[i] <= self.eps)[0]
            
            if len(neighbors) < self.min_samples:
                self.labels_[i] = -1  
            else:
                self._expand_cluster(i, neighbors, cluster_id, dist_matrix)
                cluster_id += 1

        self.core_samples_ = np.where(self.labels_ != -1)[0]
        self.noise_ = np.where(self.labels_ == -1)[0]  

    def _expand_cluster(self, point_idx, neighbors, cluster_id, dist_matrix):
        self.labels_[point_idx] = cluster_id
        seeds = neighbors.tolist()  

        while seeds:
            current_point = seeds.pop()

            if self.labels_[current_point] == -1:  
                self.labels_[current_point] = cluster_id

            if self.labels_[current_point] != -1:
                continue

            current_neighbors = np.where(dist_matrix[current_point] <= self.eps)[0]

            if len(current_neighbors) >= self.min_samples:
                seeds.extend(current_neighbors)

            self.labels_[current_point] = cluster_id

    def predict(self, data):
        if self.labels_ is None:
            raise ValueError("Модель еще не обучалась.")
        
        dist_matrix = euclidean_distances(data)
        labels = []
        
        for i in range(len(data)):
            neighbors = np.where(dist_matrix[i] <= self.eps)[0]
            if len(neighbors) >= self.min_samples:
                labels.append(self.labels_[neighbors[0]])  
            else:
                labels.append(-1)  

        return np.array(labels)

    def plot_clusters(self, data):
        plt.figure(figsize=(8, 6))
        unique_labels = np.unique(self.labels_)

        for label in unique_labels:
            cluster = data[self.labels_ == label]
            if label == -1:
                plt.scatter(cluster[:, 2], cluster[:, 3], color='black', label="Шум")
            else:
                plt.scatter(cluster[:, 2], cluster[:, 3], label=f"Кластер {int(label)+1}")

        plt.legend()
        plt.xlabel('T')
        plt.ylabel('P')
        plt.title("Кластеризация с помощью DBSCAN")
        plt.show()

    def plot_clusters_3d(self, data, elev=20, azim=30):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        unique_labels = np.unique(self.labels_)

        for label in unique_labels:
            cluster = data[self.labels_ == label]
            if label == -1:  
                ax.scatter(cluster[:, 2], cluster[:, 3], cluster[:, 4], color='black', label="Шум")
            else: 
                ax.scatter(cluster[:, 2], cluster[:, 3], cluster[:, 4], label=f"Кластер {int(label)+1}")

        ax.set_xlabel('T')
        ax.set_ylabel('P')
        ax.set_zlabel('U')
        ax.set_title("Кластеризация с помощью DBSCAN в 3D")
        ax.legend()

        ax.view_init(elev=elev, azim=azim)

        plt.show()
