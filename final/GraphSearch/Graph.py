import queue
import random as r
import graphviz as gz
import imageio as io

class Node:

    def __init__(self,label):
        self.f = -1
        self.d = 0
        self.p = None
        self.color = 'w'
        self.label = label

class Graph:

    def __init__(self):
        self.V = []
        self.adj = []

    def addNode(self):
        sz = len(self.V)
        self.V.append(Node(sz))
        self.adj.append([])
        
    def addEdge(self,source,destinations):
        
        for dest in destinations:
            self.adj[source].append(self.V[dest])

    def populate(self):
        for i in range(0,10):
            self.addNode()
        for i in range(0,10):
            A = []
            for j in range(0,10):
                if j is not i and r.randint(0,1) == True:
                    A.append(j)
            self.addEdge(i,A)

