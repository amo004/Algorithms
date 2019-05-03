import RBtree
import pickle
import os
import sys

def init(filename,persistent = True):

    if os.path.exists(filename) and persistent:
        tree = pickle.load(filename)
    else:
        tree = RBtree.RBtree()
    return tree


def ops(tree,flag,nums):
    if flag == 'i':
        for num in nums:
            tree.RB_Insert(RBtree.Node(key=int(num)))
    else:
        for num in nums:
            tree.RB_Delete(int(num))

def save(tree,filename):
    pickle.dump(tree,filename)

def parse(strs):
    for word in strs:
        if ".pickle" in word:
            filename = word
    
    if 'i' in strs:
        i = strs.index('i')

    if 'd' in strs:
        i = strs.index('d')

    return filename, i

def main(strs):
    fn, i = parse(strs)

    pers = True
    if '_' in fn:
        fn = fn.strip("_")
        pers = False

    tree = init(fn,pers)

    nums = [int(n) for n in strs[i+1:]]
    
    ops(tree,strs[i],nums)

    save(tree,fn)

if __name__ == "__main__":
    main(sys.argv)
