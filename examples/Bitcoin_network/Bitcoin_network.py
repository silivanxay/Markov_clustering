import networkx as nx

from src.Markov_clustering import ClusteringProbDist

subgraph = nx.read_edgelist('4000nodes.csv', delimiter=',', nodetype=str, data=(('weight', float),),
                            create_using=nx.DiGraph())

subgraph = nx.convert_node_labels_to_integers(subgraph, first_label=0, label_attribute='old_label')
subgraph = subgraph.to_undirected()

print('number of Nodes:', len(subgraph.nodes))
print('number of Nodes:', subgraph.number_of_edges())

clusters = ClusteringProbDist(subgraph, num_cluster=3, topN=0.2, iter=0, alpha=0, dw=0, t=0, mu_f=0)
