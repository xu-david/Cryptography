# -*- coding: utf-8 -*-
"""
Question 3: RSA Problem 5.16
"""

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
    
def rsa_common_mod_decryption(n, b1, b2, y1, y2):
    c1 = modinv(b1, b2)
    c2 = (c1*b1-1) // b2
    x1 = pow(y1, c1) * modinv(pow(y2, c2), n) % n
    print(c1, c2, x1)
    
    return x1

if __name__ == '__main__':
    n = 18721
    b1 = 43
    b2 = 7717
    y1 = 12677
    y2 = 14702
    x = rsa_common_mod_decryption(n, b1, b2, y1, y2)
    print(x)