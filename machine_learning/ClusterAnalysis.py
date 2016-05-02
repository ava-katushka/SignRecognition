from collections import defaultdict

__author__ = 'ava-katushka'
import matplotlib.pyplot as plt
import numpy as np

import plotly.plotly as py

from machine_learning.clustering import ClusterBuilder


class CharacterInCluster:
    def __init__(self, sign, n_clusters):
        self.sign = sign
        self.n_clusters = n_clusters
        self.in_clusters = [0] * n_clusters

    def picturesCount(self):
        return sum(self.in_clusters)

    def inClusersCount(self):
        result = 0
        for pic_in in self.in_clusters:
            if pic_in != 0:
                result += pic_in
        return result


class Cluster:
    def __init__(self, num):
        self.num = num
        self.pic_num = defaultdict(lambda: 0)


class ClusterAnalysis:
    def __init__(self, y, y_clusters, n_clusters):
        self.y = y
        self.y_clusters = y_clusters
        self.n_clusters = n_clusters
        self.char_dict = {}
        for sign, cl_num in zip(y, y_clusters):
            if sign in self.char_dict:
                self.char_dict[sign].in_clusters[cl_num] += 1
            else:
                self.char_dict[sign] = CharacterInCluster(sign, n_clusters)

    def cluster_description(self, cluster):
        desc_name = "Cluster " + str(cluster.num) + " description"
        print desc_name
        hist_vector = []
        for key, value in cluster.pic_num.items():
            if key:
                print "{} pictures occurs {} times".format(key, value)
                hist_vector += [key] * value
        print "--------"
        plt.hist(hist_vector, range=(0, 10))
        plt.title(desc_name)
        plt.xlabel("How many pictures")
        plt.ylabel("Times appeared")
        plt.show()


    def character_analysis(self):
        pic_in_cluster = defaultdict(lambda: 0)
        hist_count = []
        for char in self.char_dict.values():
            count = 0
            for pic_in in char.in_clusters:
                if pic_in != 0:
                    count += 1
            pic_in_cluster[count] += 1
            hist_count.append(count)
        print "CHARACTER ANALYSIS:"
        for key, value in pic_in_cluster.items():
            print "{} pictures were in {} clusters".format(value, key)
        print "------"
        plt.hist(hist_count, range=(0, 10))
        plt.title("Character Analysis")
        plt.xlabel("Clusters count")
        plt.ylabel("Pictures count")
        plt.show()

    def statistics(self):
        clusters = [0] * self.n_clusters
        for i in xrange(self.n_clusters):
            clusters[i] = Cluster(i)

        for char in self.char_dict.values():
            for i in xrange(self.n_clusters):
                clusters[i].pic_num[char.in_clusters[i]] += 1

        print "CLUSTER ANALYSIS"
        for i in xrange(self.n_clusters):
            self.cluster_description(clusters[i])


if __name__ == "__main__":
    n_clusters = 10
    analysis = ClusterAnalysis(ClusterBuilder.y, ClusterBuilder.kMeans(n_clusters), n_clusters)
    analysis.statistics()
    analysis.character_analysis()
