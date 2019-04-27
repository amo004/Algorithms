# This file implements all of the sorting algorithms
# for Algorithms exam 1 with additional frills
# for IO, so that you can check your code tracing
# the code in this file is intended to be run
# dynamically in a python shell to create examples
# for studying

import random


class Array:
    def __init__(self,size=0,min=0,max=9,zeros=False):

        self.initialized = False
        self.A = []
        if size > 0:
            self.randomArr(size,min,max)
            if zeros == True:
                for x in range(0,size):
                    self.A[x] = 0
    # imposing 1-indexed arrays
    def __getitem__(self,key):
        return self.A[key-1]
    # imposing 1-indexed arrays
    def __setitem__(self,key,value):
        if key == self.end:
            self.A.append(value)
            self.end = self.end+1
        else:
            self.A[key-1] = value

    def copy(self,a,b):
        ret = Array()

        for x in range(a,b+1):
            ret.A.append(self[x])
        ret.end = len(ret.A)+1
        return ret

    def append(self,B):
        for x in B.A:
            self.A.append(x)
        self.end = len(self.A)+1

    def swap(self,a,b):
        temp = self[a]
        self[a] = self[b]
        self[b] = temp

    def randomArr(self,size,min=0,max=9):
        self.initialized = True
        self.end = size+1
        for x in range(0,size):
            self.A.append(random.randint(min,max))

    def show(self):
        print(self.A)

    def size(self):
        return len(self.A)

    def insertionSort(self,verbose = False):
        """
            worst case \Theta(n^2)
            best case \Theta(n)
        """
        if verbose:
            print("initial Array")
            self.show()
            print("")

        for x in range(2,self.end):
            if verbose:
                print("x = ",x)
            for y in range(x,1,-1): # x downto 1
                if self[y] < self[y-1]:
                    self.swap(y,y-1)
                    if verbose:
                        self.show()
                else:
                    if verbose:
                        print("breaking")
                    break
            print("")

    def merge(self,p,q,r,verbose=False):
        """
            \Theta(n) runtime
        """
        n1 = q - p + 1
        n2 = r - q

        L = Array(n1)
        R = Array(n2)

        for x in range(1,L.end):
            L[x] = self[p + x - 1]
        for x in range(1,R.end):
            R[x] = self[q + x]

        # initializing sentinel values
        R[R.end] = float("inf")
        L[L.end] = float("inf")

        j = 1
        i = 1
        if verbose:
            print("L")
            L.show()
            print("")
            print("R")
            R.show()
            print("")

        for x in range(p,r+1):

            if L[i] <= R[j]:
                self[x] = L[i]
                if verbose:
                    self.show()
                i = i + 1
            elif R[j] < L[i]:
                self[x] = R[j]
                if verbose:
                    self.show()
                j = j+1

    def mergeSort(self,p,r,verbose=False):
        """
            \Theta(n lg n) runtime in avg and worst case
            \Theta(n) runtime in best case
        """
        if p < r:
            q = int((p+r)/2)
            self.mergeSort(p,q,verbose = verbose)
            self.mergeSort(q+1,r,verbose=verbose)
            self.merge(p,q,r,verbose=verbose)

    def isMaxHeap(self):
        """
            check if self is a heap
            for testing purposes only
        """
        for i in range(1,int(self.size()/2)+1):
            if self[i] < self[2*i]:
                return False
            if 2*i + 1 < self.size():
                if self[i] < self[2*i + 1]:
                    return False
        return True

    def maxHeapify(self,i,verbose=False):
        """
            \Theta(lg n) worst case
            \Theta(h) on a node of height h
        """
        max = i

        # left child of 1-indexed array
        if 2*i <= self.end-1:
            if self[i] < self[2*i]:
                max = 2*i
        # right child of 1-indexed array
        if 2*i + 1 <= self.end-1:
            if self[max] < self[2*i+1]:
                max = 2*i+1
        if not max == i:
            self.swap(i,max)
            if verbose:
                self.show()
            self.maxHeapify(max,verbose=verbose)

    def buildMaxHeap(self,verbose=False):
        """
            linear runtime
        """
        length = self.size()
        for x in range(int(length/2),0,-1): # floor(length/2) downto 1
            self.maxHeapify(x,verbose=verbose)

    def heapsort(self,verbose=False):
        """
            \Theta(n lg n) runtime
        """
        self.buildMaxHeap(verbose=verbose)

        # using self.end as self.heapSize
        for x in range(1,self.size()):
            self.swap(1,self.end-1)
            self.end = self.end-1
            self.maxHeapify(1,verbose = verbose)
        self.end = self.size()+1

    def heapIncreaseKey(self,index,key,verbose = False):
        """
            \Theta(lg n) worst case runtime
        """
        if key < self[index]:
            return False
        self[index] = key
        i = index
        while int(i/2) > 0: # floor(i/2)
            if self[i] > self[int(i/2)]:
                self.swap(i,int(i/2))
                i = int(i/2)
                if verbose:
                    self.show()
            else:
                return True

    def heapInsert(self,key,verbose=False):
        """
            lg n runtime
        """
        self[self.end] = key -1
        self.heapIncreaseKey(self.end-1,key,verbose=verbose)

    def heapMax(self):
        return self[1]

    def heapExtractMax(self,verbose=False):
        self.swap(1,self.end-1)
        self.end = self.end-1
        self.maxHeapify(1)
        return self.A.pop()

    def partition(self,p,r,verbose=False):
        """
            linear runtime all cases
        """
        i = p-1
        for j in range(p,r):
            if self[j] <= self[r]:
                i = i + 1
                self.swap(j,i)
        self.swap(i+1,r)
        return i+1

    def quicksort(self,p,r):
        """
            n^2 runtime worst case
            n lg n runtime average case
        """

        if p < r:
            q = self.partition(p,r)
            self.quicksort(p,q-1)
            self.quicksort(q+1,r)

    def countingSort(self,max,verbose = False):
        """
            \Theta(n+max) runtime
        """
        c = [0]*(max+1)

        for x in range(1,self.end):
            c[self[x]] = c[self[x]] + 1
        for x in range(1,max+1):
            c[x] = c[x] + c[x-1]
        B = Array(size=self.size(),zeros=True)
        for x in range(self.end -1 ,0,-1): # n downto 1
            B[c[self[x]]] = self[x]
            c[self[x]] = c[self[x]] -1
        if verbose:
            print("c")
            print(c)
            print("")
            print("b")
            B.show()
        return B

    def getDigit(self,index,digit):
        number = self[index]
        number = number%(10**digit) - number%(10**(digit-1))
        number = number /(10**(digit-1))
        return number

    def radixSort(self,digits,verbose = False):
        """
            \Theta(digits*(n+10)) runtime
        """
        max=9
        for d in range(1,digits+1):
            c = [0]*(max+1)

            for x in range(1,self.end):
                c[self.getDigit(x,d)] = c[self.getDigit(x,d)] + 1
            for x in range(1,max+1):
                c[x] = c[x] + c[x-1]
            B = Array(size=self.size(),zeros=True)
            for x in range(self.end -1 ,0,-1): # n downto 1
                B[c[self.getDigit(x,d)]] = self[x]
                c[self.getDigit(x,d)] = c[self.getDigit(x,d)] -1
            if verbose:
                print("c")
                print(c)
                print("")
                print("b")
                B.show()
            self.A = B.A


if __name__=="__main__":
    a = Array(20,min=0,max=9999)
    a.radixSort(4)
    a.show()
