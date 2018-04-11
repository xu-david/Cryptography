#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''CIPHER 2 PERMUTATION'''

import string
from collections import Counter
from itertools import zip_longest, permutations

def ioc(s):
    #incidence of coincidence
    c = Counter(s)
    n = len(s)
    t = 0.0
    for k, v in c.items():
        t += (v * (v - 1))
    return t / (n * (n - 1))

def grouper(iterable, n, fillvalue=''):
    #get fixed chunks, from py3 docs
    args = [ iter(iterable) ] * n
    return zip_longest(*args, fillvalue=fillvalue)

def unscramble_permutation(c):
    l = []
    m = len(c)
    for x in grouper(cipherstr, m):
        #print(x)
        y = [ x[i].lower() for i in c]
        l.append(''.join(y))
    l = ''.join(l)
    
    plaintxt = list(ciphertxt)
    for i, j in zip(l, lreplace):
        plaintxt[j] = i
    
    return (''.join(plaintxt))

if __name__ == '__main__':
    cipherfile = 'hw1-ciphers/cipher2.txt'
    
    with open(cipherfile) as f:
        lines = [ x for x in f.readlines() ]
        ciphertxt = ''.join(lines)

    #no punctuation
    alphabet = string.ascii_uppercase    
    cipherstr = [ x for x in iter(ciphertxt) if x in alphabet]
    cipherstrj = ''.join(cipherstr)
    lreplace = []
    for i, x in enumerate(ciphertxt):
        #print(i, x, x in alphabet)
        if x in alphabet:
            lreplace.append(i)
    
    '''#letter and ioc analysis
    #check letter frequency
    print('single letter freq')
    for k, v in sorted(Counter(cipherstr).items(), key=lambda x: x[1], reverse=1):
        print(k, v, v/len(cipherstr))
    print('-'*10)
    
    #find length of m using ioc analysis, m<=10
    print('ioc', ioc(cipherstrj))
    for m in range(2, 11):
        #print(m)
        l = [ [] for _ in range(m) ]
        for s in grouper(cipherstrj, m):
            #print(s)
            for i, j in enumerate(s):
                l[i].append(j)
        
        for i in range(m):
            s = ''.join(l[i])
            print(m, i, ioc(s))
    '''
    
    '''
    #brute force by hand
    #7 < m <= 10
    m = 7
    for c in permutations(range(m), m):
        plaintxt = unscramble_permutation(c)
        print(c, plaintxt)
    '''
    
    
    #print tab delimited m
    m = 9
    #for x in grouper(cipherstrj, m):
    #    print('\t'.join(x))
    
    
    c = (3, 4, 0, 8, 6, 1, 7, 5, 2)
    plaintxt = unscramble_permutation(c)
    print(plaintxt)