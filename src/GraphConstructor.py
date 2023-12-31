# -*- coding: utf-8 -*-
"""
@author: Matteo Pisani
This module contains some utility functions to build graphs and graphs' text encodings following
the edge list convention.
"""

from src.Graph import Graph
import numpy as np


def build_graph(file_name):
    """
    Creates and returns a graph object from the edge list contained in the given path.

    Parameters
    ----------
    file_name : string
        The relative path (from the dataset folder) to the file containing the graph definition.

    Returns
    -------
    graph : Graph
        The graph built from file_name.

    """
    with open(file_name) as file:
        lines = file.readlines()

    graph = Graph()

    for line in lines:
        [parent, child] = line.strip().split(',')
        graph.add_edge(parent, child)

    return graph

def generate_edge_list(num_nods, num_edges, name):
    """
    It creates a randomly generated edge list with a given number of nodes and of edges.
    The .txt file is saved inside the 'dataset' folder under the given name.

    Parameters
    ----------
    num_nods : int
        The number of different nodes of the graph.
    num_edges : int
        The number of total edges of the graph.
    name: string
        The name of the file we want to save.

    Returns
    -------
    None.

    """
    edges = []
    
    for i in range(num_edges):
        head = np.random.choice(num_nods)
        tail = np.random.choice(num_nods)
        edges.append((head, tail))
    
    with open("../dataset/" + name + ".txt", "w") as file:
        for edge in edges:
            file.write(f"{edge[0]},{edge[1]}\n")
    

