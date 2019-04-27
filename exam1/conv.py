
def conv(number,base,max):
    out = ''
    for i in range(1,max+1):
        val = number % (base**i)
        for j in range(0,len(out)):
            val = val - ord(out[j])*(base**j)

        val = val/(base**(i-1))
        print(val)
        out = str(chr(val)) + out

    return out

print(conv(10,7,2))
