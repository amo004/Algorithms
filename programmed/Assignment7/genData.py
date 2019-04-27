import random as r
import sys

def gen(num,uB,maxR):
    fn = "input.r.txt"
    with open(fn,"w") as f:
        arr = []
        f.write(str(num) + " " + str(uB)+ "\n")
        for id in range(1,num+1):
            string = str(id) + " "
            lb = r.randint(0,uB-1)
            ub = r.randint(lb+1,uB)
            val = r.randint(1,maxR)
            string = string + str(lb) + " "
            string = string + str(ub) + " "
            string = string + str(val)
            f.write(string+"\n")



        


if __name__ == "__main__":
    gen(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))











