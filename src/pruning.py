def pruning_of_raw_cluster_S_vq(query_nodes_cluster, top_entropy_nodes, query_nodes, exception_nodes, mt,
                                query_nodes_cluster_aggregation):
    # written by Phetsouvanh Silivanxay
    valid_cluster = []
    count = 0
    for cluster in query_nodes_cluster:
        [num_of_high_entropy,
         high_entropy_node,
         max_prob_node,
         count_majority,
         is_contained_all_top_entropy] = assign_statistic_high_entropy_node(top_entropy_nodes, query_nodes, count,
                                                                            cluster, query_nodes_cluster_aggregation,
                                                                            mt)

        if query_nodes[count] in top_entropy_nodes or is_contained_all_top_entropy:
            max_majority = 0
            max_majority_cluster = 0
            for i in range(len(query_nodes_cluster_aggregation)):
                if max_majority < count_majority[i]:
                    max_majority = count_majority[i]
                    max_majority_cluster = i
            iterable_cluster = list(cluster)
            for i in range(len(query_nodes_cluster_aggregation)):
                if i != max_majority_cluster:
                    for node in iterable_cluster:
                        if node in query_nodes_cluster_aggregation[i]:
                            cluster.remove(node)
        if num_of_high_entropy > 1 and not is_contained_all_top_entropy:
            for node in high_entropy_node:
                if node != max_prob_node and node in cluster:
                    cluster.remove(node)
            exception_nodes.append(query_nodes[count])
        count = count + 1
        valid_cluster.append(cluster)
    return valid_cluster


def is_contained_all_top_entropy_nodes(top_entropy_nodes, query_node, cluster):
    # written by Phetsouvanh Silivanxay
    contained = True
    for node in cluster:
        if node != query_node and node not in top_entropy_nodes:
            contained = False
    return contained


def assign_statistic_high_entropy_node(top_entropy_nodes, query_nodes, count, cluster, query_nodes_cluster_aggregation, mt):
    num_of_high_entropy = 0
    high_entropy_node = []
    max_prob = 0
    max_prob_node = 0
    count_majority = dict()
    is_contained_all_top_entropy = is_contained_all_top_entropy_nodes(top_entropy_nodes,
                                                                      query_nodes[count],
                                                                      cluster)
    for i in range(len(query_nodes_cluster_aggregation)):
        count_majority[i] = 0
    for node in cluster:
        if query_nodes[count] in top_entropy_nodes or is_contained_all_top_entropy:
            for i in range(len(query_nodes_cluster_aggregation)):
                if node in query_nodes_cluster_aggregation[i]:
                    count_majority[i] = count_majority[i] + 1

        if node in top_entropy_nodes and node != query_nodes[count]:
            num_of_high_entropy = num_of_high_entropy + 1
            high_entropy_node.append(node)
            current_prob_node = mt[query_nodes[count]][node]

            if max_prob < current_prob_node:
                max_prob = current_prob_node
                max_prob_node = node

    return [num_of_high_entropy, high_entropy_node, max_prob_node, count_majority, is_contained_all_top_entropy]
