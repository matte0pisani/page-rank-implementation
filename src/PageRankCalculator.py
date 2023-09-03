# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 19:02:39 2023

@author: matte
"""
import numpy as np
import src.GraphConstructor as gc
    
def PMatrix(graph, v):
    # transpose and normalize the adiacency matrix
    AT = graph.adiacency_matrix().T
    D = np.diag(AT.sum(axis=0))
    P = np.matmul(AT, np.linalg.pinv(D))
    
    return P

def pageRank(graph, alpha=0.85, v=None, algo="iterative", rround="yes"):
    # for the meaning of the variables, see PR1 paper
    if algo == "exact":
        return pageRank_exact(graph, alpha, v)
    
    N = len(graph.nodes)
    P = PMatrix(graph, v) # this P still doesn't account for sink nodes
    c = np.sum(P, axis=0) == 0
    x_0 = np.repeat(1.0/N, N)
    dangling = np.repeat(1.0/N, N)
    if v is None:
        v = np.repeat(1.0/N, N)
    
    threshold= 1e-16
    error = 1
    
    while error > threshold:
        x = alpha*(P @ x_0 + (np.inner(c, x_0) * dangling)) + (1-alpha) * v
        error = np.linalg.norm((x - x_0), ord=1) # which loss function to use?
        x_0 = x
    
    if rround == "yes":
        return np.round(x, 3)
    else: 
        return np.array(x)

# TO REVIEW
def pageRank_exact(graph, alpha, v): 
    P = PMatrix(graph, v)   
    N = len(graph.nodes)
    x = np.linalg.solve(np.eye(N,N) - alpha*P, (1-alpha)*(np.zeros(N)+v))
    
    return x
   
        
if __name__ == '__main__':

    g = gc.build_graph("../dataset/graph_5.txt")
    alpha = 0.85
    v = 1/len(g.nodes)
    PR = pageRank(g, alpha, v, rround="no")
    
    print(PR)
    