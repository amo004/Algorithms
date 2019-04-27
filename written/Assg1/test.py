
def poly(n,m,T0,k):

    #polyV = -k
    #for i in range(0,n-2):
        #polyV = polyV*m - k
    return T0*(m**(n-1)) + k * (1 - m**(n-1))/(m-1)


def recurr(n,m,T0,k):
    if n == 1:
        return T0
    else:
        return m*recurr(n-1,m,T0,k) - k

for n in range(1,10):
    print("poly = " + str(poly(n,3,2,4)) + " recurr = " + str(recurr(n,3,2,4)))
