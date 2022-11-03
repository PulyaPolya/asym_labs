import random
import math
def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]
def bit_to_byte(sequence):
    n = len(sequence)
    resulting_len = math.floor(n/8)
    bait_arr = []
    rest = n %8
    for i in range(0,n - rest, 8):
        bin = sequence[i: i+8]
        res = int("".join(str(x) for x in bin), 2)
        bait_arr.append(res)
    if rest > 0:
        residue = sequence[-rest:]
        arr = [0]*(8-rest)
        arr += residue
        res = int("".join(str(x) for x in arr), 2)
        bait_arr.append(res)
    return bait_arr

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
            #return 'prime'
        else:
            for i in range(s):
                x_d = x_d **2
                x_d = x_d %p
                if x_d == p-1:
                    pseudo_prime = True
                    #return 'prime'
                elif x_d == 1:
                    return 'not prime'
        if pseudo_prime == False:
                return 'not prime'
    return 'prime'

def generate_prime(n0, n1, k=100):
    for i in range(k):
        x = generate_number([n0, n1])
        m0 = x if x % 2 == 1 else x + 1
        interval = int((n1 - m0)/2)
        for j in range(interval):
            p = m0+ 2*j
            if miller_rabin(p) == 'prime':
                return p

def generate_p(n0, n1):
    p  = generate_prime(n0, n1)
    i = 1
    p_new = 2 * p * i + 1
    res = miller_rabin(p_new)
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
    e = 2**16+1
    d  = pow(e, -1, phi)
    secret = {'d':d, 'p':p, 'q':q}
    public = {'n' :n,'e' :e}
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
def send_key(n, k,d, e_bob, n_bob):
    if n > n_bob:
        return 'wrong n'
    k1 = pow(k, e_bob, n_bob)
    S = pow(k,d,n)
    S1 = pow(S, e_bob, n_bob)
    return (k1, S1)
def receive_key(S1, k1, n_bob, d_bob):
    k = pow(k1, d_bob, n_bob)
    S = pow(S1, d_bob, n_bob)
    return (k,S)
m = 1234

secret, public = generate_keys(2**100, 2**101)
print(secret, public)
n = public["n"]
e = public["e"]
d = secret['d']
p = secret['p']
q = secret['q']
#
print(f'n: {n}, e: {e}, m: {m}')
print(f'n_hex: {hex(n)[2:]}, e_hex: {hex(e)[2:]}, m_hex: {hex(m)[2:]}, d_hex :{hex(d)[2:]},'
      f' p_hex:{hex(p)[2:]}, q_hex:{hex(q)[2:]}')
# n = 0x221943b
# e = 0x10001
# d = 0x1885481
# p = 0x1885481
# q = 0x1543
# # code = 0xE759B3
# # print(decode(code, d, n))
# # cypher = cypher(m,e,n)
# # print(hex(cypher)[2:])
# # message = decode(c, d,n)
# # print(message)
# public_exp = 0x10001
# modulus= 0x1A60A3D072F80899EABDDB2EA0619A0DF
# # code = cypher(m, public_exp,modulus)
# # print(hex(code))
# signature_bob = 0x2E2EE9D3B8AA931CB240F9A13C5D3B10
# # print(verify(m,signature_bob, public_exp,modulus))
# # signature_alice= sign(m, d, n)
# # print(hex(signature_alice[0]))
# k = 0x123456
# res = send_key(n, k,d, public_exp, modulus)
# print(hex(res[0])[2:], hex(res[1])[2:])
# numbers = list(range(2,100))
# for n in numbers:
#     print(n,' ', miller_rabin(n))
