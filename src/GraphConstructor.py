# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 18:50:01 2023

@author: matte
"""

from Graph import Graph


def build_graph(file_name):
    with open(file_name) as file:
        lines = file.readlines()

    graph = Graph()

    for line in lines:
        [parent, child] = line.strip().split(',')
        graph.add_edge(parent, child)
    
    graph.sort_nodes()

    return graph
