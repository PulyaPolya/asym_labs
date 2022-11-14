import random
import math
from bitarray.util import int2ba
import struct
from bitarray.util import ba2int



def generate_number(range):
    r = random.randint(range[0], range[1])
    return r

def factor(p):
    a = int2ba(p)
    s = 0
    while a[-1] ==0:
        s+=1
        a.pop(-1)
    i = ba2int(a)
    return(s,i)
def miller_rabin(p):
    k = 50
    s,d = factor(p-1)
    #arr_x = [2,3,5,7]
    for i in range(k):

        x = generate_number([1,p-1])
        gcd = math.gcd(p,x)
        if gcd >1 :
            return 'not prime'
        pseudo_prime = False
        x_d = pow(x,d,p)
        if x_d == 1 or x_d == p-1:
            pseudo_prime = True
        else:
            for i in range(s):
                x_d =pow(x_d,2,p)
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
def receive_key(S1, k1, n1, d1, n):

    k = pow(k1, d1, n1)
    S = pow(S1, d1, n1)
    if k == pow(S, e,n):
        return ('true', k,S)
    return (k,S)
m = 0xaa

secret, public = generate_keys(2**256, 2**258)
print(secret, public)
n = public["n"]
e = public["e"]
d = secret['d']
p = secret['p']
q = secret['q']

print(f'n: {n}, e: {e}, m: {m}')
print(f'n_hex: {hex(n)[2:]}, e_hex: {hex(e)[2:]}, m_hex: {hex(m)[2:]}, d_hex :{hex(d)[2:]},'
      f' p_hex:{hex(p)[2:]}, q_hex:{hex(q)[2:]}')
# n = 0x8d4d97983d44f6b0456bf6b383bf0d7d1fb0d00ba7d0b7d7d2bf7d383d194668df448327023c14a462d6744f0b935c10981701a16fa7f5abfc5fb696dd1c9ee105f5
# e = 0x10001
# d = 0x7f219486f0791fca306b96a6a49e3c309b56a59817007ea7bb8175d427849a08b76f3295dc989c70944e3aad86153101c0cb585242b86ae3bde454577dea180b1471
# p = 0x14596e7a5001c21f23d6d770bccda5b10f960faeb5bf8ece95337bb6c62de5c2bef
# q = 0x6f1a12bc5b7c8ac5c4b53d4fe900245a68d64e59e04a5b51532ae87d7bacf1185b
# public_exp = 0x10001
# modulus= 0xB492E58FA2BF2B5FDDF20DABEA38A23A6B6ED27DE675945ADE169895D34FA637B3EF946F637C44949249501E35B643D25D40E235E41888DF4449B8ACD3D0CE1ED34EF5FC63E4E68F2CD03F
# modulus_little = 0x1CC4857513437109824B0198AEAE160B3
# code = 0x3D418A2EB7B2F007159725F57345181B19FE76655B96890B76F26B4897056932C3609BDBBA041670A0345060C24FCA9930AB3DE74219A0431301A0ED9EE8E5BB3C35
# print(hex(decode(code, d, n)))

# code = cypher(m, public_exp,modulus)
# print(hex(code))
# signature_bob = 0x8B83051B09CA24737C8AF754A1A9F89225CFDDD949DE230C3D5312285F8CFC066EF043EF709B79BF3240F67EF4CAA83FC415264542BECFC13C88D14A9F7F669B975393E8623F58E7697054
# print(verify(m,signature_bob, public_exp,modulus))
# signature_alice= sign(m, d, n)
# print(hex(signature_alice[0]))
# k = 0x123456
# k1, S1 = send_key(n, k,d, public_exp, modulus)
# print(hex(k1))
# print(hex(S1))
S1  =0x36F50588B9040A9F3257089B1298629DC3FF251755FD585D1E79B6198046E6A108A663A1B1533C0C2089E01996B90003E059B1A5F530AC48F41A96BC8D53927C7765
k1 = 0x57E3E087AEF37057388A4138204D0F2AF4A63F94D58BAD3C6CB57394A0ECE4A8652D300B8CC5805CAA384939FFFA7635BCEC1C74C268AD68CE6F728F77D1CCF45D69
print(receive_key(S1, k1, n, d, modulus_little))
# cypher = cypher(m,e,n)
# print(hex(cypher)[2:])
# message = decode(c, d,n)
# print(message)
