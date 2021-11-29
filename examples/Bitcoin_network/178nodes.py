import csv
import networkx as nx

from src.Markov_clustering import clustering_based_probability_distribution
from src.export import export_clusters

reader = csv.reader(open("178nodes.csv"), delimiter=",")

L = []
for row in enumerate(reader):
    L.append(row[1][1:])
adjlist = [list(map(float, adj)) for adj in L[1:]]

nbnodes = len(adjlist)

min_value = 1
for i in range(nbnodes):
    for j in range(nbnodes):
        if adjlist[i][j] != 0 and min_value > adjlist[i][j]:
            min_value = adjlist[i][j]

E = [(i, j, {'weight': 1}) for i in range(nbnodes) for j in range(nbnodes) if not (adjlist[i][j] == 0)]

di_subgraph = nx.DiGraph()
# nodes, they are added separately from edges in case there are isolated nodes
di_subgraph.add_nodes_from(range(nbnodes))
# edges
di_subgraph.add_edges_from(E)
subgraph = nx.convert_node_labels_to_integers(di_subgraph, first_label=0)

print('number of Nodes:', len(subgraph.nodes))
print('number of Nodes:', subgraph.number_of_edges())

clusters = clustering_based_probability_distribution(subgraph, num_cluster=3, top_n_nodes=0.2, iter=0,
                                                     alpha=0, dw=0, t=0, mu_f=0)

ref_file = '179nodes_result.csv'
export_clusters(ref_file, clusters)
