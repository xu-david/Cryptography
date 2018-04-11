# -*- coding: utf-8 -*-
"""
hw3, problem 4 - elliptical curve
"""

def ecc(x, p):
    #ecc(2, 11) = 5
    return (pow(x, 3) + x + 6) % p

def legendre_symbol(z, p):
    #legendre_symbol(5, 11) = 1
    return pow(z, (p-1)//2, p)

def legendre_sqrt(z, p):
    #legendre_sqrt(5, 11) = (4, 7)
    x = pow(z, (p+1)//4, p)
    return x % p, (p-x) % p

def egcd(a, b):
    s, t, r = 0, 1, b
    s0, t0, r0 = 1, 0, a
    while r != 0:
        q = r0 // r
        r0, r = r, r0 - q * r
        s0, s = s, s0 - q * s
        t0, t = t, t0 - q * t
    return r0, s0, t0

def modinv(a, m):
    #28^-1 mod 75 = modinv(28, 75) = 67
    r, s, t = egcd(a, m)
    if r != 1:
        return None
    else:
        return s % m

def calc_alpha_point(i, j, a, p):
    #calc alpha power from i = (x1, y1) and j = (x2, y2) in mod p
    if i == j:
        #slope = (3 * x1^2 + a) * (2 * y1 )^-1 mod p
        s = ((3 * pow(i[0], 2) + a) * modinv(2 * i[1], p)) % p
    else:
        #slope = (y2-y1) * (x2-x1)^-1 mod p
        s = ((j[1] - i[1]) * modinv(j[0] - i[0], p )) % p
    
    #x3 = s^2 - x1 - x2
    x3 = (pow(s, 2)  - i[0] - j[0]) % p
    
    #y3 = s (x1 - x3) - y1
    y3 = (s * (i[0] - x3) - i[1]) % p
    
    #print(s, (x3, y3))
    return x3, y3
    
if __name__ == '__main__':
    #y^2 = x^3 + ax + b (mod p)
    a = 1
    b = 6
    p = 1039
    
    lpoints = []
    for x in range(p):
        z = ecc(x, p)
        s = legendre_symbol(z, p)
        if s == 1: #quad residue
            ly = legendre_sqrt(z, p)
            for y in ly:
                lpoints.append((x, y))
                #print((x, y))
    print('a. size:', len(lpoints))
    print('b. max:', max(lpoints))
    print('c. (1014, 291) in E:', (1014, 291) in lpoints )
    
    #part d
    alpha = (799, 790)
    beta = (385, 749)
    ptxt = (575, 419)
    k = 100
    
    #y1 = k * alpha
    y1 = alpha
    for i in range(2, k + 1):
        y1 = calc_alpha_point(y1, alpha, a, p)
    
    #y2 = x + k * beta
    y2 = beta
    for i in range(2, k + 1):
        y2 = calc_alpha_point(y2, beta, a, p)
    y2 = calc_alpha_point(ptxt, y2, a, p)
    
    print('d. encryption:', y1, y2)
    
    #x = y2 - k*y1
    y1 = (873, 233)
    y2 = (234, 14)
    k = 100
    
    #k * y1
    y1k = y1
    for i in range(2, k + 1):
        y1k = calc_alpha_point(y1k, y1, a, p)
    
    #y2 - y1
    y1k = (y1k[0], -1 * y1k[1] % p)
    x = calc_alpha_point(y2, y1k, a, p)
    print('e. decryption', x)
    
    #part e diffie hellman key exchange
    #Alice a -> A = a * alpha -> send A
    #Bob b -> B = b * beta -> send B
    #K = a* b * alpha
    
    alpha = (818, 121)
    A = (199, 72) #a * alpha
    B = (815, 519) #b * alpha
    
    keyA = alpha
    for i in range(2, p + 1):
        keyA = calc_alpha_point(alpha, keyA, a, p)
        if keyA == A:
            iA = i
            break
    
    #alice key
    print('alice a: ', iA, '; keyA: ', keyA)
    keyK = B
    keyK = calc_alpha_point(keyA, keyK, a, p)
    print('shared secret: ', keyK)