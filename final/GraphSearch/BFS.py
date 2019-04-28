import Graph as g
import os
import queue
import imageio as io
import graphviz as gz

def BFS(G,s):
    time = 0
    s.d = 0
    cnt = 0
    view(G,cnt)
    Q = queue.Queue()
    Q.put(s)
    while not Q.empty():
        a = Q.get()
        
        for v in G.adj[a.label]:
            
            if v.color == 'w':
                v.p = a
                v.color = 'g'
                v.d = a.d + 1
                Q.put(v)
        cnt = cnt + 1
        a.color = 'b'
        view(G,cnt)
    animate(cnt)
    
def animate(cnt):
    ims = []
    for x in range(0,cnt+1):
        ims.append(io.imread("BFS" + str(x) + ".png"))
    kwargs = {'duration':1}
    io.mimsave("rbt.gif",ims,**kwargs)
    
    mydir = '.'
    filelist = [ f for f in os.listdir(mydir) if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))
    
def view(graph,n):
    
    G = gz.Digraph("DFS",filename="temp.gv",format="png")
    
    colors = {'w':'azure','b':'darkslategrey','g':'lightgrey'}
    for node in graph.V:
        G.node(chr(node.label + 65),style='filled',color=colors[node.color],
                label = chr(node.label + 65) + str(node.d))
    for x in range(0,len(graph.V)):
        for node in graph.adj[x]:
            if node.p is graph.V[x]:
                col = 'red'
            else:
                col = 'black'

            G.edge(chr(graph.V[x].label + 65),chr(node.label + 65),color=col)
    G.render(filename="BFS"+str(n),view = False,cleanup = True)

if __name__ == "__main__":
    graph = g.Graph()
    graph.populate()
    BFS(graph,graph.V[0])
