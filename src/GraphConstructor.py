# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:50:01 2023

@author: matte
"""

from src.Graph import Graph


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
