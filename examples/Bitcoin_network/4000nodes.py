import networkx as nx

from src.Markov_clustering import clustering_based_probability_distribution
from src.export import export_clusters

subgraph = nx.read_edgelist('4000nodes.csv', delimiter=',', nodetype=str, data=(('weight', float),),
                            create_using=nx.DiGraph())

subgraph = nx.convert_node_labels_to_integers(subgraph, first_label=0, label_attribute='old_label')
subgraph = subgraph.to_undirected()

print('number of Nodes:', len(subgraph.nodes))
print('number of Nodes:', subgraph.number_of_edges())

clusters = clustering_based_probability_distribution(subgraph, num_cluster=3, top_n_nodes=0.2, iter=0,
                                                     alpha=0, dw=0, t=0, mu_f=0)

ref_file = '4000nodes_result.csv'
export_clusters(ref_file, clusters)