## encryptor contains an encryptor decryptor and hasher

# currently finished encrypt and decrypt:
# -ceasar cypher

# currently finished hasher:
# -polinomial hash


def ceasar_encrypt(string=str,shift=int(4))->str:
    out = ""
    for s in string:
        # ord converts chars to numbers
        # chr converts numbers to chars
        out = out + chr(shift + ord(s))
    return out

def ceasar_decrypt(string=str,shift=int(4))->str:
    out = ""
    for s in string:
        # ord converts chars to numbers
        # chr converts numbers to chars
        out = out + chr(-shift + ord(s))
    return out

def polynomial_hash(string=str,base = 31,modulus=1_000_000_007)->int:# the variable in the function are defaults
    # i found this hashing algorithm in the internet
    hashval= 0
    for i , cha in enumerate(string):
        hashval = (hashval + (ord(cha) * (base**i)))%modulus
    return hashval


if __name__ =="__main__":

    l = 23
    pooop = "fishhing"
    print(l)
    x = ceasar_encrypt("fishing hill",l)
    print(x)
    y = ceasar_decrypt(x,l)
    print(y)
    print(polynomial_hash(pooop))