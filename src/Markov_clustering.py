import time

from src.Markov_centrality import Ht
from src.cluster_aggregation import cluster_aggregation
from src.utility import get_bottom_n_nodes, get_remaining_node_sorted_by_lowest_entropy, returning_S_vq
from src.pruning import pruning_of_raw_cluster_S_vq

SINGLE_NODE = 1


def clustering_based_probability_distribution(subgraph, num_cluster, top_n_nodes, iter, alpha, dw, t, mu_f):
    # written by Phetsouvanh Silivanxay
    tt = time.time()
    N = subgraph.order()
    if N == SINGLE_NODE:
        return list(subgraph.nodes)

    # mt is probability matrix
    # Hinf, mt
    Hinf, mt, Pkcg = Ht(subgraph, alpha, dw, t, mu_f)

    # FO: changed the line above to take the exact of nodes rather than a percentage
    top_entropy_nodes = get_bottom_n_nodes(Hinf, top_n_nodes, True)

    remaining_nodes = get_remaining_node_sorted_by_lowest_entropy(Hinf, False)

    clusters = __generate_query_nodes_cluster_aggregation(remaining_nodes, N, mt, num_cluster, top_entropy_nodes)
    for i in range(iter):
        query_nodes_cluster_aggregation = (clusters, mt, num_cluster, Hinf, Pkcg)
        clusters = query_nodes_cluster_aggregation

    elapsed = time.time() - tt
    print('clustering_based_probability_distribution-Completed time in secs', elapsed)

    return clusters


def __generate_query_nodes_cluster_aggregation(remaining_nodes, N, mt, num_cluster, top_entropy_nodes):
    exception_nodes = []
    query_nodes_cluster_aggregation = []
    while len(remaining_nodes) > 0:
        query_nodes = []
        for each_node in remaining_nodes:
            query_nodes.append(each_node)
            break
        S_vq = returning_S_vq(query_nodes, N, mt, num_cluster)
        pruned_S_vq = pruning_of_raw_cluster_S_vq(S_vq, top_entropy_nodes, query_nodes,
                                                  exception_nodes, mt, query_nodes_cluster_aggregation)

        pruned_S_vq.extend(query_nodes_cluster_aggregation)
        query_nodes_cluster_aggregation, included_set = cluster_aggregation(pruned_S_vq)
        included_set = included_set.union(exception_nodes)

        for each_node in included_set:
            if each_node in included_set and each_node in remaining_nodes:
                remaining_nodes.remove(each_node)
    return query_nodes_cluster_aggregation
