# A Modular Framework for Centrality and Clustering in Complex Networks
  
We consider the generalized setting of directed weighted graphs, such that
any undirected graph and/or unweighted graph can be treated as special cases.
We adhere to the definition of entropic centrality, which treats a node as central if
there is a high uncertainty about the destination of a random walker starting its
walk at the given node, where however a suitable probability to choose a given edge
by a random walker is introduced in order to capture the weights of outgoing edges,
with the further possibility to also assign an intrinsic initial weight (importance)
to nodes based on its weight cumulated out-degree.

![Probability distribution based graph clustering](images/Probability_distribution_based_graph_clustering.png)

![Pruning of the raw clustering S_vq](images/Pruning_of_the_raw_clustering_S_vq.png)


## To install libraries
```
pip install -r requirements.txt
```

## Clustering algorithm
```
import Markov_clustering import clustering_based_probability_distribution

clusters = clustering_based_probability_distribution(subgraph, num_cluster_used_by_sklearn=3, top_n_nodes=0.2, iter=0,
                                                     alpha=0, dw=0, t=0, mu_f=0)
# subgraph - the subgraph to be clustered.
#
# num_cluster_used_by_sklearn - number of cluster that would be used in SKlearn- agglomeration algoirhtm based.
#
# top_n_nodes= 0.2 - portion of high centrality nodes appeared.
#
# iter - number of iteration for aggolmeartive clustering based probability distribution.
#
# alpha is a flag:
    # alpha = 0 means the graph is considered unweighted, i.e. alpha(w(e)) = 1 for all edges e
    # use alpha = 0 if the graph is actually unweighted
    # alpha = 1 means that we use the weights of the graph, i.e. alpha(w(e)) = w(e) for all edges e
# dw defines the matrix of auxiliary probabilities
    # dw = 0 means that the function Dunif is called
    # dw > 0 means that dw*I is used as the matrix
#
# t is the time, if t==0, the asymptotic behaviour is computed
#
# mu_f is a flag:
    # mu_f = 0 means that we use a non-weighted entropy
    # mu_f = 1 means that we use an entropy weighted by the ratio of weighted out-degree by degree
    # mu_f = 2 means that we use an entropy weighted by the ratio of log2 weighted out-degree by log2 degree
```