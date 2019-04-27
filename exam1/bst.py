import random


class node:

    def __init__(self,key=None,parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

class bst:

    def __init__(self,arr=None):
        self.vals = []
        self.root = None

    def build(self,size=10,min=0,max=10):
        for x in range(0,size):
            self.insert(random.randint(min,max))

    def show(self):
        print(self.vals)

    def insert(self,key):
        self.vals.append(key)
        y = None
        x = self.root

        while not x is None:
            y = x
            if key < x.key:
                x = x.left
            else:
                x = x.right
        z = node(key=key,parent=y)
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z


    def search(self,node,key):

        x = node
        if x is None or x.key == key:
            return x

        elif x.key < key:
            return self.search(x.left,key)
        else:
            return self.search(x.right,key)

    def maximum(self,node):
        if node.right is None:
            return node
        else:
            return self.maximum(node.right)

    def minimum(self,node):
        if node.left is None:
            return node
        else:
            return self.minimum(node.left)

    def successor(self,node):

        if node.right is not None:
            return self.minimum(node.right)

        x = node
        y = node.parent
        while y is not None and y.right is x:
            x = y
            y = y.parent
        return y

    def predecessor(self,node):

        if node.left is not None:
            return self.maximum(node.left)

        x = node
        y = x.parent
        while y is not None and y.left is x:
            x = y
            y = y.parent

        return y

    def inorder(self,node):

        # empty tree
        if node is None:
            return

        if node.left is not None:
            self.inorder(node.left)

        print(node.key,end=" ")

        if node.right is not None:
            self.inorder(node.right)

    def preorder(self,node):

        print(node.key,end = " ")

        if node.left is not None:
            self.preorder(node.left)

        if node.right is not None:
            self.preorder(node.right)

    def postorder(self,node):

        if node.left is not None:
            self.postorder(node.left)

        if node.right is not None:
            self.postorder(node.right)

        print(node.key,end=" ")


    def transplant(self,u,v):
        if u.parent is None:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent



    def delete(self,node):
        if node is None:
            return
        # if you are a leaf
        if node.right is None and node.left is None:
            self.transplant(node,None)
        elif node.left is None:
            self.transplant(node,node.right)
        elif node.right is None:
            self.transplant(node,node.left)
        else:
            x = self.maximum(node.left)
            node.key = x.key
            self.delete(x)





if __name__ == "__main__":
    a = bst()
    a.build(max = 999)
    a.inorder(a.root)

    a.delete(a.root)
    print("")
    a.inorder(a.root)
    print("")
