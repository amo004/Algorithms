import graphviz as gz
import imageio as io


"""
    Author: Andrew Osborne 

    This file implements a red black tree with insertion and
    deletion. I have created this because none of the things
    I found online agreed with Cormen's algorithm and therefore
    were not good learning tools for this course.
    
    I am using graphviz to draw images representing trees,
    and I was able to install it with 

    sudo apt install python3-graphviz

    I have written some code which will take all of teh 
    generated images and sew them together in to a gif,
    but it didn't work well because of how graphviz
    handles image sizes. That code is inside
    animate and is the only thing that uses imageio,
    so you can omit that dependency if you don't care to
    try it.

    Properties of Red-Black Trees
      Every node is red or black
      every leaf (None) is black
      The root is black
      if a node is red, all both of its children are black
      All simple paths from some node to some leaf contain
        the same number of black nodes 
"""

class Node:
    # Graphs are full of nodes. This is a node
    def __init__(self,key = None,parent = None):
        self.color = 'r'
        self.key = key
        self.p = parent
        self.left = None
        self.right = None

class RBtree:
    """
        Okay, there is some wierdness afoot here, and I'll 
        tell you why. python's None is a great flag in 
        and of itself, but it throws errors when you 
        try to access some member variable of None, 
        and the algorithms in the text rely on the fact that
        None.color = black, so I had to create a 'None'
        value to use statically with this problem.

        Other than that, almost everything is exactly as
        in the text, even down to variable names and
        stuff, except my code doesn't say 
        "and the other statement is symmetric.. figure
        it out"

    """

    # sentinel value
    NIL = Node()
    NIL.color = 'b'

    def __init__(self):
        self.n = 0
        self.root = RBtree.NIL

    def inOrder(self,x,A):
        """
        returns: None
        modifies A by reference

            in order traversal to create some
            enumerable list from which to 
            create a graph
        """
        if x is RBtree.NIL: 
            return 
        self.inOrder(x.left,A) # left subtree
        A.append(x) # self
        self.inOrder(x.right,A) # right subtree

    def inOrderToString(self):
        """
            This is actually a misleading variable name.
            This was created to do something other than 
            what it ended up doing. This will take 
            your graph and save it to a png file,
            enumerating all `screenshots' of your 
            graph so that you know what happened 
            in what order
        """

        # used to store a list of nodes
        A = []

        # get that list of nodes
        self.inOrder(self.root,A)

        # this is the part that uses graphviz
        #              name           tempfile    file_format
        G = gz.Digraph("RBT",filename='temp.gv',format='png')
        # if it is unclear what this does, run it one time
        # and you will see

        
        # what color is a given node?
        for node in A:
            if node.color == 'r':
                col = 'red'
            else:
                col = 'lightgrey'
            
            # add vertices to graph and give them labels
            G.node("n" + str(node.key),style='filled',color=col,label = str(node.key))

        # draw the edges. You can modify this a bit to see the 
        # graphs like in the text with the single leaf
        for node in A:
            if node.left is not RBtree.NIL:
                G.edge("n" + str(node.key),"n" + str(node.left.key))
            if node.right is not RBtree.NIL:
                G.edge("n" + str(node.key),"n" + str(node.right.key))

        # make and save the picture
        #        start_all_files_with   render_at_runtime, delete i
        G.render(filename = "RBT" + str(self.n),view=False,cleanup=True)

        # keep track of how many pictures saved
        self.n = self.n + 1


    # this is trivial, and we beat it to death in class
    def Left_Rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left is not RBtree.NIL:
            y.left.p = x
        y.p = x.p

        if x.p is RBtree.NIL:
            self.root = y
        elif x is x.p.left:
            x.p.left = y
        else:
            x.p.right = y

        y.left = x
        x.p = y

    def Right_Rotate(self,x):
        y = x.left
        x.left = y.right

        if y.right is not RBtree.NIL:
            y.right.p = x
        y.p = x.p
        
        if x.p is RBtree.NIL:
            self.root = y
        elif x is x.p.right:
            x.p.right = y
        else:
            x.p.left = y

        y.right = x
        x.p = y


    def RB_Insert_Fixup(self,z):
        # modifies tree and fixes in accordance with the text
        while z.p.color == 'r':
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color == 'r':
                    z.p.color = 'b'
                    y.color = 'b'
                    z.p.p.color = 'r'
                    z = z.p.p
                else:
                    if z is z.p.right:
                        z = z.p
                        self.Left_Rotate(z)
                    z.p.color = 'b' 
                    z.p.p.color = 'r'
                    self.Right_Rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color == 'r':
                    z.p.color = 'b'
                    y.color = 'b'
                    z.p.p.color = 'r'
                    z = z.p.p
                else:
                    if z is z.p.left:
                        z = z.p
                        self.Right_Rotate(z)
                    z.p.color = 'b' 
                    z.p.p.color = 'r'
                    self.Left_Rotate(z.p.p)
        self.root.color = 'b'




    def RB_Insert(self,z):
        z.right = RBtree.NIL
        z.left  = RBtree.NIL

        y = RBtree.NIL
        x = self.root
        while x is not RBtree.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right 
        z.p = y

        if y is RBtree.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        z.left = RBtree.NIL
        z.right = RBtree.NIL
        z.color = "r"
        self.inOrderToString()

        self.RB_Insert_Fixup(z)
        self.inOrderToString()

    def RB_Transplant(self,u,v):
        if u.p == RBtree.NIL:
            self.root = v
        elif u is u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def RB_Delete_Fixup(self,x):
        while x is not self.root and x.color == 'b':
            if x is x.p.left:
                w = x.p.right
                if w.color == 'r':
                    w.color = 'b'
                    x.p.color = 'r'
                    self.Left_Rotate(x.p)
                    w = x.p.right
                    self.inOrderToString()
                if w.left.color == 'b' and w.right.color == 'b':
                    w.color = 'r'
                    x = x.p
                    self.inOrderToString()
                else:
                    if w.right.color == 'b':
                        w.left.color = 'b'
                        w.color='r'
                        self.Right_Rotate(w)
                        w = x.p.right
                        self.inOrderToString()
                    w.color = x.p.color
                    x.p.color = 'b'
                    w.right.color = 'b'
                    self.Left_Rotate(x.p)
                    self.inOrderToString()
                    x = self.root
                    self.inOrderToString()
            else:
                w = x.p.left
                if w.color == 'r':
                    w.color = 'b'
                    x.p.color = 'r'
                    self.Right_Rotate(x.p)
                    w = x.p.left
                    self.inOrderToString()
                    self.inOrderToString()
                if w.right.color == 'b' and w.left.color == 'b':
                    w.color = 'r'
                    x = x.p
                    self.inOrderToString()
                else:
                    if w.left.color == 'b':
                        w.right.color = 'b'
                        w.color='r'
                        self.Left_Rotate(w)
                        w = x.p.left
                        self.inOrderToString() 
                    w.color = x.p.color
                    x.p.color = 'b'
                    w.left.color = 'b'
                    self.Right_Rotate(x.p)
                    x = self.root
                    self.inOrderToString()

        x.color = 'b'
        self.inOrderToString()

    def Tree_Minimum(self,x):
        while x.left is not RBtree.NIL:
            x = x.left
        return x

    def search(self,key,node = None):
        if node is None:
            node = self.root
        if node is RBtree.NIL:
            return None
        if node.key == key:
            return node
        elif node.key < key:
            return self.search(key,node=node.right)
        else:
            return self.search(key,node=node.left)



    def RB_Delete(self,key):
        
        z = self.search(key)
        if z is None:
            return

        y = z
        y_original_color = y.color
        if z.left is RBtree.NIL:
            x = z.right
            self.RB_Transplant(z,z.right)
        elif z.right is RBtree.NIL:
            x = z.left
            self.RB_Transplant(z,z.left)
        else:
            y = self.Tree_Minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.p is z:
                x.p = y
            else:
                self.RB_Transplant(y,y.right)
                y.right = z.right
                y.right.p = y
            self.RB_Transplant(z,y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        self.inOrderToString()
        if y_original_color == 'b':
            self.RB_Delete_Fixup(x)

    def animate(self):
        """
            This will pool all of the generated
            png images and make a gif, but it 
            doesn't look great, so I'm not using
            it in the main call
        """
        ims = []
        for x in range(0,self.n):
            ims.append(io.imread("RBT" + str(x) + ".png"))
        io.mimsave("rbt.gif",ims)

if __name__ == "__main__":
    T = RBtree()
    for x in range(0,10):
        n = Node(key=x)
        T.RB_Insert(n)
    T.RB_Delete(3)
    T.RB_Delete(7)
    T.inOrderToString()
    # T.animate()
