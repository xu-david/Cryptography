#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HW5 Part 2 PGM
"""

import numpy as np
from collections import defaultdict
from sympy.combinatorics import Permutation
    
def pgm(x):
    '''
    #slide example pgm(49) = 34
    dalpha = {
        0 : {
            0 : Permutation([0, 1, 2, 3, 4]),
            1 : Permutation([1, 2, 3, 4, 0]),
            2 : Permutation([2, 3, 4, 0, 1]),
            3 : Permutation([3, 4, 0, 1, 2]),
            4 : Permutation([4, 0, 1, 2, 3]),
            },
        1 : {
            0 : Permutation([0, 1, 2, 3, 4]),
            1 : Permutation([0, 2, 1, 4, 3]),
            2 : Permutation([0, 3, 1, 2, 4]),
            3 : Permutation([0, 4, 1, 3, 2]),
            },
        2 : {
            0 : Permutation([0, 1, 2, 3, 4]),
            1 : Permutation([0, 1, 3, 4, 2]),
            2 : Permutation([0, 1, 4, 2, 3]),
            },
        }

    dbeta = {
        0 : {
            0 : Permutation(0, 3, 1, 2, 4),
            1 : Permutation(2, 4, 3),
            2 : Permutation(0, 1, 4, 3, 2),
            3 : Permutation(4)(0, 2)(1, 3),
            4 : Permutation(0, 4, 2, 3, 1),
            },
        1 : {
            0 : Permutation(1, 2)(3, 4),
            1 : Permutation(1, 4, 2),
            2 : Permutation(4)(1, 3, 2),
            3 : Permutation(4),
            },
        2 : {
            0 : Permutation(4),
            1 : Permutation(2, 4, 3),
            2 : Permutation(2, 3, 4),
            },
        }
    dpm = defaultdict(dict)
    dpm[0][0] = 0
    dpm[0][1] = 1
    dpm[0][2] = 2
    dpm[0][3] = 3
    dpm[0][4] = 4
    dpm[1][0] = 0
    dpm[1][1] = 5
    dpm[1][2] = 10
    dpm[1][3] = 15
    dpm[2][0] = 0
    dpm[2][1] = 20
    dpm[2][2] = 40
    x = 49
    '''
    
    #calculate lambda^-1
    lambdainv = []
    lalphacap = []
    for i in sorted(dpm.keys(), reverse=1):
        q, x = divmod(x, dpm[i][1])
        #print(i, q, x, dpm[i][1])
        lambdainv.insert(0, q)
        lalphacap.insert(0, dalpha[i][q])
    #print(lambdainv)
    
    #calculate alpha cap
    alphacap = combine_permutation(lalphacap)
    #print(alphacap, list(alphacap))
    
    #calculate each beta term
    betatotal = 0
    for i, pi in sorted(dbeta.items()):
        ltmp1 = [ (j, list(pij)) for j, pij in sorted(pi.items()) ]
        for x, y in enumerate(list(alphacap)):
            ltmp2 = [ b for b in ltmp1 if b[1][x] == y ]
            
            if len(ltmp2) == 1:
                break
            elif len(ltmp2) == 0:
                ltmp2 = ltmp1
        else:
            print(x, y, list(alphacap), ltmp1)
            raise Exception

        assert(len(ltmp2) == 1)
        j, betaij = ltmp2[0]
        betaijinv = ~Permutation(betaij)
        alphacap = alphacap * betaijinv
        betatotal += dpm[i][j]
        #print(i, j, dpm[i][j], alphacap)
    return betatotal

def combine_permutation(l):
    o = l[-1] * l[-2]
    if len(l) > 2:
        for i in l[-3::-1]:
            o = o * i
    return o

def read_log_signature(filename, blocks, s):
    with open(filename) as f:
        lines = []
        for x in f:
            x = [ int(i) - 1 for i in x.split() ]
            lines.append(x)
    dalpha = defaultdict(dict)
    dbeta = defaultdict(dict)
    c = 0
    for i in range(s):
        for j in range(blocks - i):
            #print(i, j, lines[c])
            dalpha[i][j] = Permutation(lines[c][:10])
            dbeta[i][j] = Permutation(lines[c][10:])
            c += 1
    return dalpha, dbeta

if __name__ == '__main__':    
    #read cipher into 1-D list
    lmap = [' ']
    with open('ciphers/PGM_problem_matrix.txt') as f:
        for x in f:
            x = x.split()
            lmap += x
    dmap = {} #int -> char, char -> int
    for i, j in enumerate(lmap):
        dmap[j] = i
        dmap[i] = j
    
    #read logarithmic signatures
    blocks = 10
    s = 8
    dalpha, dbeta = read_log_signature('ciphers/PGM_logs.txt', blocks, s)

    #find p_ij m_i -> dpm
    lr = list(range(blocks, blocks - s, -1))
    lm = [1]
    for i in range(1, s+1):
        #print(i, lr[:i], np.prod(lr[:i]))
        lm.append(np.prod(lr[:i]))
    
    dpm = defaultdict(dict)
    for i, j in enumerate(lm[:-1]):
        #print(i, j, lr[i])
        for k in range(lr[i]):
            #print(i, k, k*j)
            dpm[i][k] = k*j
    
    #read ciphertext
    with open('ciphers/PGM_ciphertext.txt') as f:
        lines = ''.join([ x.rstrip() for x in f.readlines()])
    
    M = pow(95, 3)
    seed = 2000
    ki = pgm(seed)
    plaintext = ''
    for i, c in enumerate(range(0, len(lines), 3)):
        chars = list(lines[c:c+3])
        lc = list(dmap.get(x) for x in chars)
        yi = (lc[0]*95*95 + lc[1] * 95 + lc[2]) % M
        xi = (yi - ki) % M
        
        #print(i, chars, yi, ki, xi)
        
        x1, r = divmod(xi, pow(95, 2))
        x2, x3 = divmod(r, 95)
        #print(x1, x2, x3)
        x1c = dmap.get(x1)
        x2c = dmap.get(x2)
        x3c = dmap.get(x3)
        
        #print(x1c, x2c, x3c)
        plaintext = plaintext + x1c + x2c + x3c
        ki = pgm(seed+i+1)
    print(plaintext)