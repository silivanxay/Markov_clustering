def getValidQueryNodeCluster(queryNodesCluster, TopEntropyNodes, queryNodes, exceptionNodes, mt,
                             queryNodesClusterAggreation):
    # written by Phetsouvanh Silivanxay
    validCluster = []
    count = 0;
    for cluster in queryNodesCluster:
        numOfHighEntropy = 0
        highEntropyNode = []
        maxProb = 0
        maxProbNode = 0
        countMajority = dict()
        isContainedAllTopEntropy = isContainedAllTopEntropyNodes(TopEntropyNodes, queryNodes[count], cluster)

        for i in range(len(queryNodesClusterAggreation)):
            countMajority[i] = 0
        for node in cluster:
            if queryNodes[count] in TopEntropyNodes or isContainedAllTopEntropy:
                for i in range(len(queryNodesClusterAggreation)):
                    if (node in queryNodesClusterAggreation[i]):
                        countMajority[i] = countMajority[i] + 1

            if (node in TopEntropyNodes and node != queryNodes[count]):
                numOfHighEntropy = numOfHighEntropy + 1
                highEntropyNode.append(node)
                currentProbNode = mt[queryNodes[count]][node]
                # print ('highEntropyNode',queryNodes[count],node, currentProbNode)

                if (maxProb < currentProbNode):
                    maxProb = currentProbNode
                    maxProbNode = node
        if (queryNodes[count] in TopEntropyNodes or isContainedAllTopEntropy):
            maxMajority = 0  # countMajority[0]
            maxMajorityCluster = 0
            for i in range(len(queryNodesClusterAggreation)):
                if (maxMajority < countMajority[i]):
                    maxMajority = countMajority[i]
                    maxMajorityCluster = i
            iterable_cluster = list(cluster)
            for i in range(len(queryNodesClusterAggreation)):
                if (i != maxMajorityCluster):
                    for node in iterable_cluster:
                        if (node in queryNodesClusterAggreation[i]):
                            cluster.remove(node)
            # print ('validCluster',cluster)
        if (numOfHighEntropy > 1 and not isContainedAllTopEntropy):
            for node in highEntropyNode:
                if (node != maxProbNode and node in cluster):
                    cluster.remove(node)
            # print ('numOfHighEntropy >1 -> validCluster',cluster,'maxProbNode:',maxProbNode)
            exceptionNodes.append(queryNodes[count])
        count = count + 1
        validCluster.append(cluster)
        # print ('validCluster',validCluster)
    return validCluster

def isContainedAllTopEntropyNodes(TopEntropyNodes,queryNode,cluster):
    #written by Phetsouvanh Silivanxay
    contained = True
    for node in cluster:
        if( node != queryNode and node not in TopEntropyNodes):
            contained = False
    return contained