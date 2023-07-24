# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 19:02:39 2023

@author: matte
"""
import numpy as np
    
def PMatrix(graph, v):
    # transpose and normalize the adiacency matrix
    AT = graph.adiacency_matrix().T
    D = np.diag(AT.sum(axis=0))
    P_signed = AT @ np.linalg.pinv(D)
    
    # fill out dangling nodes, if any (use strongly preferential approach)
    # TO DO: how to without iteration? use c vector
    # TO DO: insert different filling strategies
    for i in range(P_signed.shape[1]):
        if np.sum(P_signed[:,i]) == 0:
            P_signed[:,i] = v
    return P_signed

def pageRank_iterative(graph, alpha, v):
    P = PMatrix(graph, v)
    x_0 = [0 for i in range(P.shape[1])] # one possible initialization
    threshold= 1e-16
    error = 1
    v = np.array(v)
    
    while error > threshold:
        x_1 = alpha*(P @ x_0) + (1-alpha)*v
        error = np.linalg.norm((x_1 - x_0), ord=1) # which loss function to use?
        x_0 = x_1
    
    return np.round(x_1,3)

def pageRank(graph, alpha, v):
    P = PMatrix(graph, v)
    N = len(graph.nodes)
    x = np.linalg.solve(np.eye(N,N) - alpha*P, (1-alpha)*(np.zeros(N)+v))
    
    return np.round(x,3)
    