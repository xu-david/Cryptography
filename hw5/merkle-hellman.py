#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merkle-Hellman public key cryptosystem
https://asecuritysite.com/encryption/knapcode
"""

import random

def miller_rabin(n, k=1000):
    '''
    miller-rabin primality test
    return true if it passes k rounds and is probably prime
    else false if composite
    '''
    r = 0
    d = n - 1
    #pow(2, r) * d = n - 1
    while not d % 2:
        r += 1
        d //= 2
    
    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for j in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                return 0
            if x == n - 1:
                break
        else:
            return 0
    return 1

def find_first_prime(n):
    '''
    find first prime number > n
    '''
    assert(n % 2) #check odd
    while 1:
        n += 2
        if miller_rabin(n):
            break
    return n

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

def solve_superincreasing_knapsack(s, l):
    r = []
    for x in sorted(l, reverse=1):
        if x <= s:
            r.append(1)
            s -= x
        else:
            r.append(0)
    r.reverse()
    return r

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
    
    #find M and W
    M = 2036764117802210446778721319780021001
    W = 127552671440279916013001
    M = find_first_prime(M) #2036764117802210446778721319780021357
    W = find_first_prime(W) #127552671440279916013021
    Winv = modinv(W, M) #717820533383415790905237126080986020
    #print(M, W, Winv)
    assert(W*Winv%M == 1)

    with open('ciphers/knapsack_cryptosystem_problem.txt') as f:
        lines = f.readlines()
        B = [ int(x.strip()) for x in lines[17:64]]
        Y = [int(x.strip()) for x in lines[68:132]]

    #find superincreasing knapsack items
    A = []
    for b in B:
        #b = W^-1 * y mod M
        a = Winv * b % M
        A.append(a)

    dmap = { j : i for i, j in enumerate(A) }
    dpermutation = {}
    for i, j in enumerate(sorted(A)):
        dpermutation[dmap.get(j)] = i
    
    output = ''
    for y in Y:
        #s = W^-1 * y mod M
        s = Winv * (y % M) % M
        r = solve_superincreasing_knapsack(s, A)
        
        x = [ r[j] for i, j in sorted(dpermutation.items()) ]
        #print(x)
        x = ''.join(map(str, x))
        x = str(int(x, 2))
        #print(x)
                
        while len(x) < 14:
            x = '0' + x
        #print(x)
            
        for c in range(0, len(x), 2):
            i = int(x[c]) #row
            j = int(x[c + 1]) #column
            output += lookup[i][j]
    print(output)