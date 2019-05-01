import Graph as g
import random as r

class UndirectedGraph(g.Graph):
    """
        This file implements a weighted, undirected
        graph by extending the earlier graph class.

        Some care has to be taken to avoid doing dumb things
        with edges and weights.
    """

    def addEdge(self,edges):
        # edges is expected to be a list of tuples with
        # no pairwise transposes
        for edge in edges:
            # append to -> from and from -> to
            self.adj[edge[0]].append(self.V[edge[1]])
            self.adj[edge[1]].append(self.V[edge[0]])

            # generate some random weights and make sure we 
            # have symmetry
            self.w[edge[0]][edge[1]] = r.randint(1,20)
            self.w[edge[1]][edge[0]] = self.w[edge[0]][edge[1]]



    def populate(self,numNodes = 10):
        # initialize weight matrix
        self.w = [[float("inf")for i in range(numNodes)] for k in range(numNodes)]

        # add nodes
        for i in range(0,numNodes):
            self.addNode()

        # generate aforementioned list of tuples
        A = []
        for i in range(0,numNodes):
            for j in range(i+1,numNodes):
                if r.randint(0,1) == True:
                    A.append((i,j))
        # print(A)
        self.addEdge(A)
