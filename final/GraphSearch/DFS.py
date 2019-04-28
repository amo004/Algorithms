import graphviz as gz
import Graph as g
import os
import imageio as io

def DFS_Visit(G,x,time):
    x.color = 'g'
    x.d = time[0]
    view(G,time[0])

    for node in G.adj[x.label]:
        if node.color == 'w':
            node.p = x
            time[0] = time[0] + 1
            DFS_Visit(G,node,time)
    time[0] = time[0] + 1
    x.f = time[0]
    x.color = 'b'
    view(G,time[0])

def DFS(G):
    for v in G.V:
        v.d = 0
        v.f = 0
        v.p = None
    # runtime of $\Theta(V + E)$
    time = [0]
    for v in G.V:
        if v.color == 'w':
            DFS_Visit(G,v,time)
    animate(time[0])

def view(graph,n):
    # generate a png of the current state of the graph 
    G = gz.Digraph("DFS",filename="temp.gv",format="png")
    
    colors = {'w':'azure','b':'darkslategrey','g':'lightgrey'}

    for node in graph.V:
        G.node(chr(node.label + 65),style='filled',
            color=colors[node.color],
            label = chr(node.label + 65) + str(node.d) + "|" + str(node.f)
            )

    for x in range(0,len(graph.V)):
        for node in graph.adj[x]:
            if node.p is graph.V[x]:
                col = 'red'
            else:
                col = 'black'
            G.edge(chr(graph.V[x].label + 65),chr(node.label + 65),color=col)

    G.render(filename="DFS"+str(n),view = False,cleanup = True)

def animate(cnt):
    # take all of the generated images and make a gif
    ims = []
    for x in range(0,cnt+1):
        ims.append(io.imread("DFS" + str(x) + ".png"))

    # increase this number to make the gif
    # move more slowly
    kwargs = {'duration':1}
    io.mimsave("dfs.gif",ims,**kwargs)
    
    # delete all of the png files you generated
    mydir = '.'
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))
 
if __name__ == "__main__":
    graph = g.Graph()
    graph.populate()
    DFS(graph)
