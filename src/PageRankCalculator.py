# -*- coding: utf-8 -*-
"""
@author: matte

This module contains the actual implementation of the algorithm on a generic graph.
"""
import numpy as np
    
def P_matrix(graph):
    """
    Compute the P matrix to use in the PageRank algorithm (see Langville and Gleich). 
    It does not embed a policy for dealing with sink nodes (their column
    is composed of all 0s); so P is a substochastic matrix (as in a psedudo-pg problem).

    Parameters
    ----------
    graph : Graph
        the graph which P refers to.
        
    Returns
    -------
    P : numpyarray
        A 2 dimensional array equal to the trasposed adjacency matrix multiplied for the
        Penrose-pseudoinverse of the D matrix.

    """
    AT = graph.adjacency_matrix().T
    D = np.diag(AT.sum(axis=0))
    P = np.matmul(AT, np.linalg.pinv(D))
    
    return P

def pageRank(graph, alpha=0.85, v=None, algo="iterative", rround="yes"):
    """
    Returns the PageRank value for each of the nodes of the given graph, using the
    given parameters. It applies the weakly preferential policy for sink nodes (the random
    surfer is teleported to a random node following a uniform distribution).

    Parameters
    ----------
    graph : Graph (own implementation)
        The graph containing the nodes to compute the PageRank for.
    alpha : float, optional
        The damping parameter of the algorithm. The default is 0.85.
    v : numpy array, optional
        Teleportation vector. Each element represent the probability of moving to a certain
        node in the teleportation step of the random surfer. The default is a uniform distribution
        over all nodes. For the meaning of v, see the papers.
    algo : string, optional
        Used to distinguish between an iterative application of the algorithm and exact one.
        For the iterative version, it applies the update rule contained in Gleich's paper until
        convergence (there is no limit of iterations). The pg values vector is initialized
        as a uniform distribution over all the nodes.
        The default value of the parameter is "iterative". For the exact version, use "exact".
    rround : string, optional
        String value to apply a rounding of the pg values to the first 3 decimal digits. 
        The default is "yes".

    Returns
    -------
    numpy array
        An array containing the pg value for each node. Each value refers to the node in graph
        which holds the same position in the graph's node list.
    """
    # TO DO implement more policies for sink nodes?
    # TO DO create iteration limit?
    # TO DO add different initializations for x_0?
    # TO DO should directly work with array or lists?
    # TO DO should return a dictionary?
    if algo == "exact":
        return pageRank_exact(graph, alpha, v, rround)
    
    N = len(graph.nodes)
    P = P_matrix(graph)
    c = np.sum(P, axis=0) == 0
    x = np.repeat(1.0/N, N)   # initialization vector
    dangling = np.repeat(1.0/N, N)  # sink nodes policy vector
    if v is None:   # teleportation vector
        v = np.repeat(1.0/N, N)
    
    threshold= 1e-16
    error = 1
    
    while error > threshold:
        x_old = x
        x = alpha*(P @ x_old + (np.inner(c, x_old) * dangling)) + (1-alpha) * v
        error = np.linalg.norm((x - x_old), ord=1)  # use norm 1 to convergence

    if rround == "yes":
        return np.round(x, 3)
    else: 
        return x

def pageRank_exact(graph, alpha=0.85, v=None, rround="yes"): 
    """
    Exact resolution for the PageRank problem. It is done by solving the linear system
    associated to the problem as shown in Gleich's paper. We still use the weakly preferential
    approach.

    Parameters
    ----------
    graph : Graph (own implementation)
        The graph containing the nodes to compute the PageRank for.
    alpha : float, optional
        The damping parameter of the algorithm. The default is 0.85.
    v : numpy array, optional
        Teleportation vector. Each element represent the probability of moving to a certain
        node in the teleportation step of the random surfer. The default is a uniform distribution
        over all nodes. For the meaning of v, see the papers.
    rround : string, optional
        String value to apply a rounding of the pg values to the first 3 decimal digits. 
        The default is "yes".

    Returns
    -------
    numpy array
        An array containing the pg value for each node. Each value refers to the node in graph
        which holds the same position in the graph's node list.

    """
    P = P_matrix(graph)   
    N = len(graph.nodes)
    if v is None:
        v = np.repeat(1.0/N, N)
    
    # this time we need to complete P as to make it a stochastic matrix
    c = np.sum(P, axis=0) == 0
    u = np.repeat(1.0/N, N)
    P = P + np.outer(u,c)
    
    x = np.linalg.solve(np.eye(N,N) - alpha*P, (1-alpha)*v)
    
    if rround == "yes":
        return np.round(x, 3)
    else: 
        return x

# TO DO: method for printing stuff
    