import operator
from sklearn import cluster


def get_bottom_n_nodes(H, n, rev):
    # written by Phetsouvanh Silivanxay
    H_dict = dict()
    for i in range(len(H)):
        H_dict[i] = H[i]
    output = get_dictionary_n_nodes_from_bottom(H_dict, n, rev)

    return output


def get_dictionary_n_nodes_from_bottom(H_dict, n, rev):
    count = 0
    output = []
    for key, value in sorted(H_dict.items(), key=operator.itemgetter(1), reverse=rev):
        if (count == n):
            break
        output.append(key)
        count = count + 1

    return output


def get_remaining_node_sorted_by_lowest_entropy(H, rev):
    # written by Phetsouvanh Silivanxay

    # select query nodes from bottom n entropy value
    included_set = []

    H_dict = dict()
    for i in range(len(H)):
        H_dict[i] = H[i]
    remainingNodes = []
    for node, value in sorted(H_dict.items(), key=operator.itemgetter(1), reverse=rev):
        if node not in included_set:
            remainingNodes.append(node)
    return remainingNodes


def returning_S_vq(query_nodes, N, mt, num_cluster):
    # written by Phetsouvanh Silivanxay
    query_nodes_cluster = []
    for queryNode in query_nodes:
        probDist = []
        index_clusters, maxIndex = find_prob_dist_cluster_with_query_node(mt, num_cluster, queryNode, N)
        query_nodes_cluster.append(index_clusters[maxIndex])

    return query_nodes_cluster


def find_prob_dist_cluster_with_query_node(prob_dist_matrix, num_cluster, node, N):
    # written by Phetsouvanh Silivanxay
    prob_dist, results = leverage_agglomerative_clustering(N, node, prob_dist_matrix, num_cluster)

    avg_result = dict()
    count_result = dict()
    index_clusters = []
    for i in range(num_cluster):
        avg_result[i] = 0
        count_result[i] = 0
        index_clusters.append([])

    for i in range(len(results[0])):
        avg_result[results[0][i]] = avg_result[results[0][i]] + prob_dist[i][0]
        count_result[results[0][i]] = count_result[results[0][i]] + 1
        index_clusters[results[0][i]].append(i)
    max_result = 0
    max_index = 0

    for i in range(num_cluster):
        if count_result[i] != 0:
            avg_result[i] = avg_result[i] / (count_result[i] + 0.0)
            if max_result < avg_result[i] != 0 and avg_result[i] != 1:
                max_result = avg_result[i]
                max_index = i
    if max_result == 0 or max_result == 1:
        index_clusters[max_index] = []
    index_clusters[max_index].append(node)
    return index_clusters, max_index


def leverage_agglomerative_clustering(N, node, prob_dist_matrix, num_cluster):
    prob_dist = []

    for i in range(N):
        if i != node:
            prob_dist.append([prob_dist_matrix[node][i], 0])
        else:
            prob_dist.append([0, 0])
    results = []
    if N > 2:
        agglomerative = cluster.AgglomerativeClustering(n_clusters=num_cluster, linkage="ward", affinity='euclidean')
        agglomerative.fit(prob_dist)

        results.append(list(agglomerative.labels_))
    else:
        agglomerative = cluster.AgglomerativeClustering(n_clusters=1, linkage="ward", affinity='euclidean')
        agglomerative.fit(prob_dist)

        results.append(list(agglomerative.labels_))
    return prob_dist, results


def get_bottom_n_clusters(H, n, rev, clusters):
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

    output = get_dictionary_n_nodes_from_bottom(H_cluster_dict, n, rev)

    return output