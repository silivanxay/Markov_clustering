from src.utility import get_bottom_n_clusters, find_prob_dist_cluster_with_query_node
from src.pruning import pruning_of_raw_cluster_S_vq


def cluster_agglomertion(clusters, mt, num_cluster, Hinf, Pkcg):
    # written by Phetsouvanh Silivanxay
    agg_clusters = []
    N = len(clusters)
    if (N == 1):
        return clusters

    N = len(clusters)

    [prob_dist_matrix, connect_matrix] = generate_cluster_prob_dist(clusters, N, mt, Pkcg)

    cluster_list = get_bottom_n_clusters(Hinf, int(N), False, clusters)
    top_entropy_cluster_list = get_bottom_n_clusters(Hinf, int(N * 0.3), True, clusters)

    query_nodes_cluster_aggregation = generate_query_nodes_cluster_aggregation(cluster_list,
                                                                                               prob_dist_matrix,
                                                                                               num_cluster, N,
                                                                                               top_entropy_cluster_list,
                                                                                               connect_matrix,
                                                                                               agg_clusters)

    mapping_back_cluster = generate_mapping_back_cluster(query_nodes_cluster_aggregation, clusters)

    query_nodes_cluster_aggregation, included_set = cluster_aggregation(mapping_back_cluster)
    return query_nodes_cluster_aggregation


def generate_cluster_prob_dist(clusters, N, mt, Pkcg):
    # written by Phetsouvanh Silivanxay
    prob_dist_matrix = [[0 for x in range(N)] for y in range(N)]
    connect_matrix = [[0 for x in range(N)] for y in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j:
                Min = 1
                connect = 0
                for nodeI in clusters[i]:
                    for nodeJ in clusters[j]:
                        if Min > mt[nodeI][nodeJ] != 0:
                            Min = mt[nodeI][nodeJ]
                        if Pkcg[nodeI][nodeJ] != 0:
                            connect = Pkcg[nodeI][nodeJ]
                prob_dist_matrix[i][j] = Min
                connect_matrix[i][j] = connect
    return [prob_dist_matrix, connect_matrix]


def generate_query_nodes_cluster_aggregation(cluster_list, prob_dist_matrix, num_cluster, N,
                                             top_entropy_cluster_list, connect_matrix,
                                             agg_clusters):
    # written by Phetsouvanh Silivanxay
    query_nodes_cluster_aggregation = []
    while len(cluster_list) > 0:
        node = []
        for each_cluster in cluster_list:
            node = each_cluster
            break
        cluster_list.remove(node)
        index_clusters, max_index = find_prob_dist_cluster_with_query_node(prob_dist_matrix, num_cluster, node, N)
        exceptionNodes = []
        index_clusters[max_index] = pruning_of_raw_cluster_S_vq([index_clusters[max_index]], top_entropy_cluster_list,
                                                                [node],
                                                                exceptionNodes, prob_dist_matrix,
                                                                query_nodes_cluster_aggregation)
        copy_indexCluster = list(index_clusters[max_index][0])
        for index in copy_indexCluster:
            if connect_matrix[node][index] == 0 and node != index:
                index_clusters[max_index][0].remove(index)

        for i in range(len(index_clusters)):
            if i == max_index:
                for index in index_clusters[i][0]:
                    if index in cluster_list:
                        cluster_list.remove(index)

                agg_clusters.append(set(index_clusters[max_index][0]))
        agg_clusters.extend(query_nodes_cluster_aggregation)
        query_nodes_cluster_aggregation, included_set = cluster_aggregation(agg_clusters)
    return query_nodes_cluster_aggregation


def generate_mapping_back_cluster(query_nodes_cluster_aggregation, clusters):
    # written by Phetsouvanh Silivanxay
    mapping_back_cluster = []

    for each_cluster in query_nodes_cluster_aggregation:
        result_set = set()
        for index in each_cluster:
            result_set = result_set.union(clusters[index])
        mapping_back_cluster.append(result_set)

    mapping_back_cluster.extend(clusters)
    return mapping_back_cluster


def cluster_aggregation(query_nodes_cluster):
    # written by Phetsouvanh Silivanxay
    query_nodes_cluster_aggregation = []
    included_set = set()
    while len(query_nodes_cluster) > 0:
        merge_cluster = []

        for single_cluster in query_nodes_cluster:
            merge_cluster = single_cluster
            break
        query_nodes_cluster.remove(merge_cluster)
        merge_cluster_set = set(merge_cluster)
        remove_clusters = []

        for single_cluster in query_nodes_cluster:
            single_cluster_set = set(single_cluster)
            if single_cluster_set.intersection(merge_cluster_set):
                merge_cluster_set = merge_cluster_set.union(single_cluster_set)
                remove_clusters.append(single_cluster)
        for item in remove_clusters:
            query_nodes_cluster.remove(item)

        query_nodes_cluster_aggregation.append(merge_cluster_set)
        included_set = included_set.union(merge_cluster_set)
    return query_nodes_cluster_aggregation, included_set
