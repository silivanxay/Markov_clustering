import time
import numpy as np

def Ht(G, alpha, dw, t, mu_f):
    tt = time.time()
    # G is the graph, nodes must be labelled by integers starting from 0,
    # use nx.convert_node_labels_to_integers(G, first_label=0) if needed
    #
    # alpha is a flag:
    # alpha = 0 means the graph is considered unweighted, i.e. alpha(w(e)) = 1 for all edges e
    # use alpha = 0 if the graph is actually unweighted
    # alpha = 1 means that we use the weights of the graph, i.e. alpha(w(e)) = w(e) for all edges e
    #
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

    # number of nodes
    n = G.order()

    def Dunif(G, alpha):
        # compute the auxiliary probabilities in a way which is proportional to the weighted degree
        n = G.order()
        if alpha == 0:
            Du = np.zeros((n, n))
            for i in range(n):
                li = list(G[i].keys())
                # nb of neighbours + self-loop + auxiliary node
                Du[i][i] = 1 / (len(li) + 2)

        if alpha == 1:
            Du = np.zeros((n, n))
            # list containing the weighted (out-)degrees
            if nx.is_directed(G):
                weighted_deg = G.out_degree(weight='weight')
            else:
                weighted_deg = G.degree(weight='weight')
            for i in range(n):
                li = list(G[i].keys())
                # nb of neighbours + self-loop + auxiliary node
                Du[i][i] = 1 / (weighted_deg[i] + 2)

        return Du

    # compute the transition probability matrices P and Ptilde
    # matrix of probabilities
    P = np.zeros((n, n))
    # initialize Ptilde
    Pt = np.zeros((n, n))
    # adjacency matrix and self-loops added
    A = nx.to_numpy_matrix(G) + np.identity(n)

    # computes the matrix of auxiliary probabilities
    D = []
    if dw == 0:
        D = Dunif(G, alpha)
    else:
        D = dw * np.identity(n)

    if alpha == 0:
        for i in range(n):
            li = list(G[i].keys())
            for j in range(n):
                if not (A[i].getA()[0][j] == 0):
                    P[i][j] = 1 / (len(li) + 1)
                    # FO
                    Pt[i][j] = P[i][j] * (1 - D[i][i])
    weighted_deg = []
    if alpha == 1:
        # list containing the weighted (out-)degrees
        if nx.is_directed(G):
            weighted_deg = G.out_degree(weight='weight')
        else:
            weighted_deg = G.degree(weight='weight')

        for i in range(n):
            li = list(G[i].keys())
            for j in range(n):
                Aij = A[i].getA()[0][j]
                if not (Aij == 0):
                    # a weight of 1 is given to the self-loop
                    P[i][j] = Aij / (weighted_deg[i] + 1)
                    Pt[i][j] = P[i][j] - D[i][i] * Aij / (weighted_deg[i] + 1)
                    # Pt[i][j] = P[i][j] - D[i][i]/(len(li)+1)

    # m contains the modified version of P, Ptilde
    mup = np.hstack((Pt, D))

    mdown = np.hstack((np.zeros((n, n)), np.identity(n)))
    m = np.vstack((mup, mdown))

    # distinguish finite from asymptotic values of t
    if t == 0:
        # asymptotic case
        mt = np.matmul(np.linalg.inv(np.identity(n) - Pt), D)
    else:
        mt = np.linalg.matrix_power(m, t)

    # define the weight mu for each node
    mu = []
    if mu_f == 0:
        mu = np.ones(n)

    if mu_f == 1:
        for u in G.nodes():
            dwout = sum([G[u][v]['weight'] for v in G.successors(u)])
            if not (dwout == G.out_degree(u)):
                # ratio of degree as weight
                mu.append(dwout / G.out_degree(u))
            else:
                mu.append(1)

    if mu_f == 2:
        for u in G.nodes():
            dwout = sum([G[u][v]['weight'] for v in G.successors(u)])
            if not (dwout == G.out_degree(u)):
                # ratio of entropic centralities as weight
                mu.append(np.log2(dwout) / np.log2(G.out_degree(u)))
            else:
                mu.append(1)

                # initialize entropy vector
    H = [0 for k in range(n)];
    if t == 0:
        # asymptotic case
        for i in range(n):
            for j in range(n):
                pij = mt[i][j]
                if pij != 0:
                    # handles numerical approximation of zero
                    if abs(pij) > 1.0e-14:
                        H[i] = H[i] - pij * np.log2(pij) * mu[j]
    else:
        # finite case
        for i in range(n):
            for j in range(n):
                pij = mt[i][j] + mt[i][n + j]
                if pij != 0:
                    H[i] = H[i] - pij * np.log2(pij) * mu[j]

    elapsed = time.time() - tt
    # print('time in secs',elapsed)
    return H, mt, P