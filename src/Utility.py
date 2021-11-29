import operator


def getBottomN(H, n, rev):
    # written by Phetsouvanh Silivanxay
    H_dict = dict()
    for i in range(len(H)):
        H_dict[i] = H[i]
    count = 0
    output = []
    for key, value in sorted(H_dict.items(), key=operator.itemgetter(1), reverse=rev):
        if (count == n):
            break
        output.append(key)
        count = count + 1

    return output


def getRemainingNodeSortedBylowestEntropy(Kcg, includedSet, H, rev):
    # written by Phetsouvanh Silivanxay
    H_dict = dict()
    for i in range(len(H)):
        H_dict[i] = H[i]
    count = 0
    remainingNodes = []
    for node, value in sorted(H_dict.items(), key=operator.itemgetter(1), reverse=rev):
        if node not in includedSet:
            remainingNodes.append(node)
    return remainingNodes


def getQueryNodeCluster(queryNodes, N, mt, num_cluster):
    # written by Phetsouvanh Silivanxay
    queryNodesCluster = []
    for queryNode in queryNodes:
        probDist = []
        indxedClusters, maxIndex = findProbdistClusterWithQueryNode(mt, num_cluster, queryNode, N)
        # print ('mini result',maxIndex, indxedClusters[maxIndex])
        queryNodesCluster.append(indxedClusters[maxIndex])

    return queryNodesCluster


def findProbdistClusterWithQueryNode(probdistMatrix, num_cluster, node, N):
    # written by Phetsouvanh Silivanxay
    probdist = []

    for i in range(N):
        if (i != node):
            probdist.append([probdistMatrix[node][i], 0])
        else:
            probdist.append([0, 0])
    results = []
    if (N > 2):
        agglomerative = cluster.AgglomerativeClustering(n_clusters=num_cluster, linkage="ward", affinity='euclidean')
        agglomerative.fit(probdist)

        results.append(list(agglomerative.labels_))
    else:
        # print('debug',N,probdist)
        agglomerative = cluster.AgglomerativeClustering(n_clusters=1, linkage="ward", affinity='euclidean')
        agglomerative.fit(probdist)

        results.append(list(agglomerative.labels_))
    # print (node,'results',results)

    avg_result = dict()
    count_result = dict()
    indxedClusters = []
    for i in range(num_cluster):
        avg_result[i] = 0
        count_result[i] = 0
        indxedClusters.append([])
    for i in range(len(results[0])):
        avg_result[results[0][i]] = avg_result[results[0][i]] + probdist[i][0]
        count_result[results[0][i]] = count_result[results[0][i]] + 1
        indxedClusters[results[0][i]].append(i)
    max = 0
    maxIndex = 0
    for i in range(num_cluster):
        if (count_result[i] != 0):
            avg_result[i] = avg_result[i] / (count_result[i] + 0.0)
            if (max < avg_result[i] and avg_result[i] != 0 and avg_result[i] != 1):
                max = avg_result[i]
                maxIndex = i
            # print (i,avg_result[i], count_result[i])
    if (max == 0 or max == 1):
        indxedClusters[maxIndex] = []
    indxedClusters[maxIndex].append(node)
    # print ('mini result',maxIndex, indxedClusters[maxIndex])
    return indxedClusters, maxIndex


def getBottomNClusters(H, n, rev, clusters):
    # written by Phetsouvanh Silivanxay
    H_dict = dict()
    for i in range(len(H)):
        H_dict[i] = H[i]
    H_cluster_dict = dict()
    for i in range(len(clusters)):
        H_cluster_dict[i] = 0
        for node in clusters[i]:
            H_cluster_dict[i] = H_cluster_dict[i] + H_dict[node]
        H_cluster_dict[i] = H_cluster_dict[i] / len(clusters[i])

    count = 0
    output = []
    for key, value in sorted(H_cluster_dict.items(), key=operator.itemgetter(1), reverse=rev):
        if (count == n):
            break
        output.append(key)
        count = count + 1

    return output