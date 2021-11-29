from sklearn import cluster
import networkx as nx
import time

def ClusteringProbDist(Kcg, num_cluster, topN, iter, alpha, dw, t, mu_f):
    # written by Phetsouvanh Silivanxay
    tt = time.time()
    N = Kcg.order()
    if N == 1:
        return list(Kcg.nodes)
    # Pkcg, D = MatrixWithAuxilary(Kcg,w)
    # Pkcg, D = MatrixWithAuxilaryFanOut(Kcg,w)
    # Hinf, mt = Hijt(Pkcg,D,t)

    # mt is probablity matrix
    # Hinf,mt
    Hinf, mt, Pkcg = Ht(Kcg, alpha, dw, t, mu_f)

    # select query nodes from bottom n entropy value
    includedSet = []
    queryNodesClusterAggreation = []

    # TopEntropyNodes = getBottomN(Hinf,int(N*topN),True)
    # FO: changed the line above to take the exact of nodes rather than a percentage
    TopEntropyNodes = getBottomN(Hinf, topN, True)

    remainingNodes = getRemainingNodeSortedBylowestEntropy(Kcg, includedSet, Hinf, False)

    exceptionNodes = []
    while (len(remainingNodes) > 0):
        queryNodes = []
        for remainingNode in remainingNodes:
            queryNodes.append(remainingNode)
            break
        # print('queryNodes',queryNodes)
        # getQueryNodeCluster is returning S_vq
        queryNodesCluster = getQueryNodeCluster(queryNodes, N, mt, num_cluster)
        # getValidQueryNodeCluster does the pruning of raw cluster S_vq
        queryNodesCluster = getValidQueryNodeCluster(queryNodesCluster, TopEntropyNodes, queryNodes, exceptionNodes, mt,
                                                     queryNodesClusterAggreation)

        queryNodesCluster.extend(queryNodesClusterAggreation)
        queryNodesClusterAggreation, includedSet = ClusterAggregation(queryNodesCluster)
        includedSet = includedSet.union(exceptionNodes)

        for eachNode in includedSet:
            if (eachNode in includedSet and eachNode in remainingNodes):
                remainingNodes.remove(eachNode)

    clusters = queryNodesClusterAggreation
    # print ('seeds.append (',queryNodesClusterAggreation,')')
    for i in range(iter):
        # print ('round:', i)
        queryNodesClusterAggreation = ClusterAgglomertion(clusters, mt, num_cluster, Hinf, Pkcg)
        clusters = queryNodesClusterAggreation
        # print ('final:',clusters)

    elapsed = time.time() - tt
    print('Complete  time in secs', elapsed)

    return clusters