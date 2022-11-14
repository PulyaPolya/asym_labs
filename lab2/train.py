# def factor(p):
#     s = 0
#     while p % 2 == 0:
#         # print(p)
#         p = p / 2
#         s += 1
#     print(s,p)
# def bitfield(n):
#     return [1 if digit=='1' else 0 for digit in bin(n)[2:]]
# p1 =2301048731286647480424212
# p2 = p1+2
# a1 = bitfield(p1)
# print(a1)
# s = 0
# while a1[-1] ==0:
#     a1.pop(-1)
#     s+=1
# print(a1)
# print(s)

from bitarray.util import int2ba
import struct
from bitarray.util import ba2int
# p = 2301048731286647480424212
# a = int2ba(p)
# print(a)
# s = 0
# while a[-1] ==0:
#     s+=1
#     a.pop(-1)
# print(s)
# i = ba2int(a)
# print(i)

def factor(p):
    a = int2ba(p)
    print(a)
    s = 0
    while a[-1] ==0:
        s+=1
        a.pop(-1)
    print(s)
    i = ba2int(a)
    return(s,i)

p = 2301048731286647480424212
s,i = factor(p)
print(s,i)
p = 2301048731286647480424214
s,i = factor(p)
print(s,i)