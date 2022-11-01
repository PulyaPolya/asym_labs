import random
import math
def generate_number(range):
    r = random.randint(range[0], range[1])
    return r

def miller_rabin(p):
    s = 0
    d = p-1
    while d % 2 == 0:
        s += 1
        d /= 2
    d = int(d)
    arr_x = [2,3,5,7]
    for x in arr_x:
        #x = generate_number([1,p-1])
        gcd = math.gcd(p,x)
        if gcd >1 :
            return 'not prime'
        pseudo_prime = False
        x_d = pow(x,d,p)
        if x_d == 1 or x_d == p-1:
            pseudo_prime = True
        else:
            for i in range(s):
                x_d = x_d **2
                x_d = x_d %p
                if x_d == p-1:
                    pseudo_prime = True
                    break
                elif x_d == 1:
                    return 'not prime'
        if pseudo_prime == False:
                return 'not prime'
    return 'prime'

def generate_prime(n0, n1, k=100):
    for i in range(k):
        x = generate_number([n0, n1])
        m0 = x if x % 2 == 1 else x + 1
        for i in range(int((n1 - m0)/2)):
            p = m0+ 2*i
            if miller_rabin(p) == 'prime':
                return p

def generate_p(n0, n1):
    p  = generate_prime(n0, n1)
    i = 1
    p_new = 2 * p * i + 1
    res = ''
    while res != 'prime':
        p_new =2 * p * i + 1
        res = miller_rabin(p_new)
        i+=1
    return p_new

def count_phi(p,q):
    return (p-1)*(q-1)

def generate_keys(n0,n1):
    p = generate_p(n0, n1)
    q = generate_p(n0, n1)
    n = p*q
    phi = count_phi(p,q)
    #e = generate_number([2, phi])
    e = 2**16+1
    d  = pow(e, -1, phi)
    secret = (d, p, q)
    public = (n,e)
    return secret, public

def cypher(m, e, n):
    return pow(m,e,n)

def decode(c,d,n):
    return pow(c,d,n)

def sign(m,d,n):
    return (pow(m,d,n),m)

def verify(m,s, e,n):
    if m == pow(s,e,n):
        return 'correct'
    else:
        return 'wrong'

# print(generate_keys(1,100))
