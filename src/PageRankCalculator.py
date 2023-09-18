# -*- coding: utf-8 -*-
"""
@author: Matteo Pisani

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
        Penrose-pseudoinverse of the D matrix (see Langville and Gleich).

    """
    AT = graph.adjacency_matrix().T
    d = AT.sum(axis=0)
    d[d == 0] = 1
    return AT / d

def pageRank(graph, alpha=0.85, max_iterations=400, algo="iterative", rround="yes"):
    """
    Returns the PageRank value for each of the nodes of the given graph, using the
    given parameters. It applies the weakly preferential policy for sink nodes (the random
    surfer is teleported to a random node following a uniform distribution). The 
    personalization vector is considered to be a uniformly distributed one.

    Parameters
    ----------
    graph : Graph (own implementation)
        The graph containing the nodes to compute the PageRank for.
    alpha : float, optional
        The damping parameter of the algorithm. The default is 0.85.
    max_iterations: int, optional
        The maximum number of iterations to do in case an iterative procedure is chosen (see
        algo parameter): when the maximum value is reached, the execution of the function stops
        and the result obtained at that point is returned. The default is 400.
    algo : string, optional
        Used to distinguish between an iterative application of the algorithm and exact one.
        For the iterative version, it applies the update rule contained in Gleich's paper until
        convergence or maximum iterations reached. The pg values vector is initialized
        as a uniform distribution over all the nodes. For the exact version, see pageRank_exact.
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
    if algo == "exact":
        return pageRank_exact(graph, alpha, rround)
    
    N = len(graph)
    P = P_matrix(graph)
    c = np.sum(P, axis=0) == 0
    v = np.repeat(1.0/N, N)  # teleportation vector
    x = v.copy()   # initialization vector
    dangling = v.copy()  # sink nodes policy vector
    
    threshold= 1e-16
    error = 1
    
    for i in range(max_iterations):
        x_old = x
        x = alpha*(P @ x_old + (np.inner(c, x_old) * dangling)) + (1-alpha) * v
        error = np.linalg.norm((x - x_old), ord=1)  # use norm 1 to convergence
        if error < threshold:
            break

    if rround == "yes":
        return np.round(x, 3)
    return x

def pageRank_exact(graph, alpha=0.85, rround="yes"): 
    """
    Exact resolution for the PageRank problem. It is done by solving the linear system
    associated to the problem as shown in Gleich's paper. We still use the weakly preferential
    approach and a uniform v vector.

    Parameters
    ----------
    graph : Graph (own implementation)
        The graph containing the nodes to compute the PageRank for.
    alpha : float, optional
        The damping parameter of the algorithm. The default is 0.85.
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
    N = len(graph)
    v = np.repeat(1.0/N, N)
    
    # this time we need to complete P as to make it a stochastic matrix
    c = np.sum(P, axis=0) == 0
    u = np.repeat(1.0/N, N)
    P = P + np.outer(u,c)
    
    x = np.linalg.solve(np.eye(N,N) - alpha*P, (1-alpha)*v)
    
    if rround == "yes":
        return np.round(x, 3)
    return x

def pageRank_pretty_print(graph, pg_values):
    """
    Prints the page rank value of each node, explicitly associating the node IDs
    with the PR value. 

    Parameters
    ----------
    graph : Graph
        The graph the PR values refer to.
    pg_values : numpy array
        The values computed over the given graph.

    Returns
    -------
    None.

    """
    print()
    print("Page rank values:")
    print("-----------------------")
    
    for i in range(len(graph.nodes)):
        print("Node", i+1, " [id: " + graph.nodes[i].name + "]:", pg_values[i])
    print()
     