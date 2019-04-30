import queue
import random as r
import graphviz as gz
import imageio as io

"""
This implements the framework datastructure that I use 
to complete graph algorithms. Not all of these algorithms
use all of these facilities
"""


class Node:

    def __init__(self,label):
        self.f = -1
        self.d = 0
        self.p = None
        self.color = 'w'
        self.label = label

class Graph:

    def __init__(self):
        # used to store Node objects which are vertices in our list
        self.V = []
        self.w = None
        # store a (shallow) copy of self.V[j] in self.adj[i]
        # to add an edge from verted i to vertex j
        self.adj = []

    def addNode(self):
        # add a node to self.V..
        # note that we must add nodes before edges
        sz = len(self.V)
        self.V.append(Node(sz))
        self.adj.append([])
        
    def addEdge(self,source,destinations,weights=None):
        if self.w is None and weights is not None:
            self.w = [[0]*len(self.V)]*len(self.V)

        for dest in destinations:
            self.adj[source].append(self.V[dest])
            if weights is not None:
                self.w

    def populate(self):
        # create a random graph with ten vertices
        # and some number of edges
        for i in range(0,10):
            self.addNode()
        for i in range(0,10):
            A = []
            for j in range(0,10):
                if j is not i and r.randint(0,1) == True:
                    A.append(j)
            self.addEdge(i,A)

    
