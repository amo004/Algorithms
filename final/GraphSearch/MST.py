import UndirectedGraph as g
import os
import imageio as io
import graphviz as gz 
"""
    This file implements prim's algorithm for finding
    minimal spanning trees. This uses an UndirectedGraph 
    instead of a directed graph, but I believe this requirement
    is somewhat superfluous 

    I don't plan to implement Kruskal's algorithm because it uses
    some data structures that I don't feel like implementing
"""

def Extract_Min(Q):
    # this really should be done with a priority
    # queue, but I don't want to implement one
    min = 0
    for x in range(0,len(Q)):
        if Q[x].key < Q[min].key:
            min = x

    return Q.pop(min)


def Prim(G,r):
    """
    Prim's algorithm, almost directly from the text
    """
    r.key = 0    
    Q = []
    for node in G.V:
        Q.append(node)

    index = 0
    view(G,index)


    while len(Q) > 0:
        u = Extract_Min(Q)
        for v in G.adj[u.label]:
            if v in Q and G.w[u.label][v.label] < v.key:
                v.p = u
                v.key = G.w[u.label][v.label]
                index += 1 
                # take a snapshot of the graph
                view(G,index)
    # make a gif 
    animate(index)


def animate(cnt):
    # take all of the generated images and make a gif
    ims = []
    for x in range(0,cnt+1):
        ims.append(io.imread("MST" + str(x) + ".png"))

    # increase this number to make the gif
    # move more slowly
    kwargs = {'duration':1}
    io.mimsave("mst.gif",ims,**kwargs)
    
    # delete all of the png files you generated
    mydir = '.'
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))
    
def view(graph,n):
    # generate a png of the current state of the graph 
    G = gz.Graph("MST",filename="temp.gv",format="png")
    
    for node in graph.V:
        G.node(chr(node.label + 65),label = str(node.key))
    for x in range(0,len(graph.V)):
        for node in graph.adj[x]:
            if node.p is graph.V[x] or graph.V[x].p is node:
                col = 'red'
            else:
                col = 'black'
            # print(graph.w) 
            if graph.V[x].label > node.label:
                G.edge(chr(graph.V[x].label + 65),chr(node.label + 65),color=col,
                   label = str(graph.w[node.label][graph.V[x].label])
                )
    G.render(filename="MST"+str(n),view = False,cleanup = True)

if __name__ == "__main__":
    graph = g.UndirectedGraph()
    graph.populate()
    Prim(graph,graph.V[0])


