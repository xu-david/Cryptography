#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import gcd, floor

def pollard_p1(n, b = 5555):
    '''
    Pollard p-1 factoring
    '''
    a = 2
    for j in range(2, b + 1):
        a = pow(a, j, n)
    d = gcd(a - 1, n)
    if 1 < d < n:
        return d
    else:
        return 0

def multiplicative_inverse(a, b):
    '''
    Using pseudocode from book
    '''
    a0 = a
    b0 = b
    t0 = 0
    t = 1
    q = floor(a0 / b0)
    r = a0 - q * b0
    while r > 0:
        temp = (t0 - q * t) % a
        t0 = t
        t = temp
        a0 = b0
        b0 = r
        q = floor(a0 / b0)
        r = a0 - q * b0
    if b0 != 1:
        return 0
    else:
        return t

if __name__ == '__main__':
    lookup = [
            [ ' ', '*', '4', '>', 'H', 'R', '\\', 'f', 'o', 'x' ],
            [ '!', '+', '5', '?', 'I', 'S', ']', 'g', 'p', 'y' ],
            [ '\\', ',', '6', '@', 'J', 'T', '^', 'h', 'q', 'z' ],
            [ '#', '-', '7', 'A', 'K', 'U', '_', 'i', 'r', '{' ],
            [ '$', '.', '8', 'B', 'L', 'V', '`', 'j', 's', '|' ],
            [ '%', '/', '9', 'C', 'M', 'W', 'a', 'k', 't', '}' ],
            [ '&', '0', ':', 'D', 'N', 'X', 'b', 'l', 'u', '~' ],
            [ '\'', '1', ';', 'E', 'O', 'Y', 'c', 'm', 'v', ' '],
            [ '(', '2', '<', 'F', 'P', 'Z', 'd', 'n', 'w', ' '],
            [ ')', '3', '=', 'G', 'Q', '[', 'e', '\n', ' ', ' ']
        ]

    n = 68102916241556970724365932142686835003312542409731911391
    b = 36639088738407540894550923202224101809992059348223191299
    
    with open('ciphers-parameter-matrix/RSA-ciphertext.txt') as f:
        ctxt = [ x.strip() for x in f ]
    
    #calculate private key variables p, q, a
    p = pollard_p1(n) #pollard p-1 -> p
    q = n // p # n = p * q
    phi_n = (p - 1)*(q - 1)
    a = multiplicative_inverse(phi_n, b)
    
    l = ''
    for y in ctxt:
        x = str(pow(int(y), a, n)) #x = y^a mod n
        if len(x) % 2:
            x = '0' + x
        for c in range(0, len(x), 2):
            i = int(x[c]) #row
            j = int(x[c + 1]) #column
            l += lookup[i][j]
    print(l)