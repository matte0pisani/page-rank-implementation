# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 12:43:56 2023

@author: matte
"""
import networkx as nx
import numpy as np
import PageRankCalculator as prc
import GraphConstructor as gc

def nx_pagerank(file_name, alfa):
    with open(file_name) as f:
        lines = f.readlines()
    
    G = nx.DiGraph()
    
    for line in lines:
        t = tuple(line.strip().split(','))
        G.add_edge(*t)
    
    pr = nx.pagerank(G, alpha=alfa) 
    # see online documentation for nx.pagerank; by default, alpha is 0.85
    # and v (should be) a uniformly distributed stochastic vector (v here 
    # should be equivalent to "personalization")
    pr = dict(sorted(pr.items(), key=lambda x: x[0]))
    return np.round(list(pr.values()), 3)

def test(file_name, alpha):
    nx_result = nx_pagerank(file_name, alpha)
    g = gc.build_graph(file_name)
    my_result = prc.pageRank(g, alpha, np.repeat(1/len(g.nodes), len(g.nodes)))
    
    diff = abs(nx_result - my_result)
    sse = np.sum(diff ** 2)
    mse = sse / len(diff)
    sum_residuals = np.sum(diff) / len(diff)
    order = np.argsort(nx_result) == np.argsort(my_result)
    return sse, mse, sum_residuals, order

# =============================================================================
# TO FIX
# nx.draw(G, with_labels=True, node_size=2000, edge_color='#eb4034', width=3, font_size=16, font_weight=500, arrowsize=20, alpha=0.8)
# plt.savefig("graph.png")
# =============================================================================

        
if __name__ == '__main__':
    
    alpha = 0.85
    result = test('../dataset/graph_5.txt', alpha)
    
    print(result[0])
    print()
    print(result[1])
    print()
    print(result[2])
    print()
    print(result[3])
