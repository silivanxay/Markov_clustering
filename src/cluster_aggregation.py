from src.utility import getBottomNClusters, findProbdistClusterWithQueryNode
from src.validation import getValidQueryNodeCluster

import random


def ClusterAgglomertion(clusters, mt, num_cluster, Hinf, Pkcg):
    # written by Phetsouvanh Silivanxay
    aggClusters = []
    N = len(clusters)
    if (N == 1):
        return clusters
    probdistMatrix = [[0 for x in range(N)] for y in range(N)]
    probdistMatrixMax = [[0 for x in range(N)] for y in range(N)]
    connectMatrix = [[0 for x in range(N)] for y in range(N)]
    for i in range(N):
        for j in range(N):
            if (i != j):
                Min = 1
                Max = 0
                Sum = 0
                connect = 0
                for nodeI in clusters[i]:
                    for nodeJ in clusters[j]:
                        if (Max < mt[nodeI][nodeJ]):
                            Max = mt[nodeI][nodeJ]
                        if (Min > mt[nodeI][nodeJ] and mt[nodeI][nodeJ] != 0):
                            Min = mt[nodeI][nodeJ]
                        if (Pkcg[nodeI][nodeJ] != 0):
                            connect = Pkcg[nodeI][nodeJ]
                        Sum = mt[nodeI][nodeJ]
                avg = Sum / (len(clusters[i]) * len(clusters[j]))
                # print (i, j,'avg:', avg,'min:',min,'max:',max)
                probdistMatrix[i][j] = Min
                probdistMatrixMax[i][j] = Max
                connectMatrix[i][j] = connect
    N = len(clusters)

    clusterList = getBottomNClusters(Hinf, int(N), False, clusters)
    TopEntropyClusterList = getBottomNClusters(Hinf, int(N * 0.3), True, clusters)
    randomList = random.sample(range(0, N), N)
    queryNodesClusterAggreation = []

    while (len(clusterList) > 0):
        node = []
        for acluster in clusterList:
            node = acluster
            break
        clusterList.remove(node)
        indxedClusters, maxIndex = findProbdistClusterWithQueryNode(probdistMatrix, num_cluster, node, N)
        exceptionNodes = []
        indxedClusters[maxIndex] = getValidQueryNodeCluster([indxedClusters[maxIndex]], TopEntropyClusterList, [node],
                                                            exceptionNodes, probdistMatrix, queryNodesClusterAggreation)
        copy_indexCluster = list(indxedClusters[maxIndex][0])
        for index in copy_indexCluster:
            if (connectMatrix[node][index] == 0 and node != index):
                indxedClusters[maxIndex][0].remove(index)
                # print ('remove not connect',indxedClusters[maxIndex][0])

        for i in range(len(indxedClusters)):
            if (i == maxIndex):
                # resultSet = set()
                # print ('indxedClusters[i][0]',indxedClusters[i][0])
                for index in indxedClusters[i][0]:
                    if (index in clusterList):
                        clusterList.remove(index)

                aggClusters.append(set(indxedClusters[maxIndex][0]))
        # print ('aggClusters',aggClusters)
        aggClusters.extend(queryNodesClusterAggreation)
        queryNodesClusterAggreation, includedSet = ClusterAggregation(aggClusters)
        # print ('final queryNodesClusterAggreation:',queryNodesClusterAggreation)

    MappingBackCluster = []

    # print ('seeds.append (',queryNodesClusterAggreation,')')
    for acluster in queryNodesClusterAggreation:
        resultSet = set()
        for index in acluster:
            resultSet = resultSet.union(clusters[index])
        MappingBackCluster.append(resultSet)

    MappingBackCluster.extend(clusters)
    queryNodesClusterAggreation, includedSet = ClusterAggregation(MappingBackCluster)
    # print ('final MappingBackCluster:',queryNodesClusterAggreation)
    return queryNodesClusterAggreation


def ClusterAggregation(queryNodesCluster):
    # written by Phetsouvanh Silivanxay
    queryNodesClusterAggreation = []
    includedSet = set()
    while (len(queryNodesCluster) > 0):
        mergeCluster = []
        for singleCluster in queryNodesCluster:
            mergeCluster = singleCluster
            break
        queryNodesCluster.remove(mergeCluster)
        mergeClusterSet = set(mergeCluster)
        removeClusters = []
        for singleCluster in queryNodesCluster:
            singleClusterSet = set(singleCluster)
            if (singleClusterSet.intersection(mergeClusterSet)):
                mergeClusterSet = mergeClusterSet.union(singleClusterSet)
                removeClusters.append(singleCluster)
        for item in removeClusters:
            queryNodesCluster.remove(item)

        queryNodesClusterAggreation.append(mergeClusterSet)
        includedSet = includedSet.union(mergeClusterSet)
    return queryNodesClusterAggreation, includedSet
