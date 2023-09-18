# -*- coding: utf-8 -*-
"""
@author: Matteo Pisani
This module is to model graphs and nodes; I added only the essential aspects of the two, without
implementing the full ADT.

"""

import numpy as np

class Graph: 
    """
    This class models a graph for the PageRank problem. It consists essentialy of a list
    of nodes. It has methods to check the presence of a node, find a node (or create one),
    link two nodes and compute the adiacency matrix.
    """
    def __init__(self):
        self.nodes = []
    
    def __len__(self):
        return len(self.nodes)
    
    def contains(self, name):
        for node in self.nodes:
            if(node.name == name):
                return True
        return False
    
    def find(self, name):
        if(not self.contains(name)):
            new_node = Node(name)
            self.nodes.append(new_node)
            return new_node
        else:
            return next(node for node in self.nodes if node.name == name)
        
    def add_edge(self, parent, child):
        parent_node = self.find(parent)
        child_node = self.find(child)

        parent_node.link_child(child_node)
        child_node.link_parent(parent_node)
        
    def adjacency_matrix(self):
        A = np.zeros((len(self.nodes), len(self.nodes)))
        for i in range(len(self.nodes)):
            children = [node.name for node in self.nodes[i].children]
            row = [node.name in children for node in self.nodes]
            A[i] = row
        return A

class Node:
    """
    This class represents a node. A node has some children and parents, which we could 
    link to using its methods.
    """
    
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        
    def __repr__(self):
        return "node " + self.name

    def link_child(self, new_child):
        for child in self.children:
            if(child.name == new_child.name):
                return None
        self.children.append(new_child)

    def link_parent(self, new_parent):
        for parent in self.parents:
            if(parent.name == new_parent.name):
                return None
        self.parents.append(new_parent)
        