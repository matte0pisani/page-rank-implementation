# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:50:01 2023

@author: matte
"""

from src.Graph import Graph
import numpy as np


def build_graph(file_name):
    with open(file_name) as file:
        lines = file.readlines()

    graph = Graph()

    for line in lines:
        [parent, child] = line.strip().split(',')
        graph.add_edge(parent, child)
    
    # graph.sort_nodes() 
    # this actually creates problems, as it is not compatible with the default
    # order with which nx orders nodes (that is queue-like). See more in test.py

    return graph

def generate_edge_list(num_nods, num_edges):
    edges = []
    
    # Generate edges for the graph
    for i in range(num_edges):
        head = np.random.choice(num_nods)
        tail = np.random.choice(num_nods)
        edges.append((head, tail))
    
    # Save the edge list to a text file
    with open("../dataset/graph.txt", "w") as file:
        for edge in edges:
            file.write(f"{edge[0]},{edge[1]}\n")
    

