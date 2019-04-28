"""
    This assumes rod prices are passed as a python list
    so that Array[i] is the price of a rod of length i+1
"""

def CutRod(p,n):
    Opt = [0]*(n+1)
    for x in range(1,n+1):
        find_opt(p,Opt,x)
    return Opt

def find_opt(p,opt,n):
    opt[n] = p[n]
    for x in range(0,n):
        opt[n] = max(p[x] + opt[n-x],opt[n])

if __name__ == "__main__":
    p = [0,1,5,8,9,10,17,17,20,24,30]
    print(CutRod(p,10))
