# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 17:09:12 2023

@author: matte
"""

import numpy as np

class Graph: 
    # note that all the creation methods are used only when initializing
    # the graph from a file
    def __init__(self):
        self.nodes = []
    
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
        
    def sort_nodes(self):
        self.nodes.sort(key=lambda node: int(node.name))
        
    def adiacency_matrix(self):
        A = np.zeros((len(self.nodes), len(self.nodes)))
        for i in range(len(self.nodes)):
            children = [node.name for node in self.nodes[i].children]
            row = [node.name in children for node in self.nodes]
            A[i] = row
        return A
            

class Node:
    # questions: 
    # should names be both strings and integers?
    # should enforce coherence (someone's son needs to have the first as father)?
    # should names be unique? How to enforce it? We are assuming only, up to now.
    
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []

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
        
    def __repr__(self):
        return "node " + self.name

