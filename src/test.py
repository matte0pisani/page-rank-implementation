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
    # pr = dict(sorted(pr.items(), key=lambda x: x[0]))
    # The point is the following. nx doesn't allow to explicitly order nodes, for what I
    # know. So it will perform the PageRank algorithm with his own order (which is queue-
    # like). Then, to order the pg values results obtained, we try to order them by using
    # the above criterion, which doesn't order like we would like. This is because, even
    # if we are ordering by key, the key is not the "names" attribute, but (for what I've
    # come to understand) an ID given by nx to the nodes based on the order they've been 
    # seen. In graph_1/2/3/4 and IBM this doesn't occur as all or most of the graphs are
    # encountered in alphabetical order.
    return np.array(list(pr.values()))

def test(file_name, alpha):
    nx_result = nx_pagerank(file_name, alpha)
    g = gc.build_graph(file_name)
    my_result = prc.pageRank(g, alpha, rround="no")
    
    diff = abs(nx_result - my_result)
    sse = np.sum(diff ** 2)
    mse = sse / len(diff)
    mean_error = np.sum(diff) / len(diff) #  maybe compare with first significative figure
    order = np.argsort(nx_result) == np.argsort(my_result)
    
    return sse, mse, mean_error, order

# =============================================================================
# TO FIX
# nx.draw(G, with_labels=True, node_size=2000, edge_color='#eb4034', width=3, font_size=16, font_weight=500, arrowsize=20, alpha=0.8)
# plt.savefig("graph.png")
# =============================================================================

        
if __name__ == '__main__':
    
    alpha = 0.85
    result = test('../dataset/graph_6.txt', alpha)
    
    print(result[0])
    print()
    print(result[1])
    print()
    print(result[2])
    print()
    print(all(result[3]))
