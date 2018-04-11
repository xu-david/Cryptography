#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''CIPHER 1 VIGNERE'''

import string
from collections import Counter
from itertools import zip_longest

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
  
if __name__ == '__main__':
    cipherfile = 'hw1-ciphers/cipher1.txt'
    
    with open(cipherfile) as f:
        lines = [ x for x in f.readlines() ]
        ciphertxt = ''.join(lines)

    #no punctuation
    alphabet = string.ascii_uppercase
    dalphabet = { i:j for i,j in enumerate(alphabet) }
    for i in list(dalphabet.keys()):
        dalphabet[dalphabet[i]] = i
    
    cipherstr = [ x for x in iter(ciphertxt) if x in alphabet]
    cipherstrj = ''.join(cipherstr)
    
    #check letter frequency
    print('single letter freq')
    for k, v in sorted(Counter(cipherstr).items(), key=lambda x: x[1], reverse=1):
        print(k, v, v/len(cipherstr))
    print('-'*10)
    
    #find length of m using ioc analysis, m=10
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
    
    #find key frequencies
    m = 10
    
    y = [ [] for _ in range(m) ]
    for s in grouper(cipherstrj, m):
        for i, j in enumerate(s):
            y[i].append(j)
          
    lfreq = [ 0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061,
              0.070, 0.020, 0.008, 0.400, 0.240, 0.067, 0.075, 0.019,
              0.001, 0.060, 0.063, 0.091, 0.028, 0.010, 0.023, 0.001,
              0.020, 0.001 ]
    
    dfreq = { i : j for i, j in zip(alphabet, lfreq)}
    
    #find each k_i
    for i in range(10):
        #print(i, y[i])
        l = [ dalphabet.get(x) for x in y[i] ]
        n = len(l)
        
        d = {}
        for j in range(26): #shift
            lt1 = [ divmod(x - j, 26)[1] for x in l ] #left shift
            lt2 = [ dalphabet.get(x) for x in lt1 ]
            
            c = Counter(lt2)
            
            mg = 0.0
            for k, v in Counter(lt2).items():
                mg += dfreq.get(k) * v / n #p_i * f_i+g / n'
            
            #print(j, mg)
            d[dalphabet.get(j)] = round(mg, 4)
        
        #K_i and sorted IOC per position
        print(i, sorted(d.items(), key=lambda x: x[1], reverse=1), end='\n\n')
        
    #guess key
    key = 'DARKKNIGHT'
    assert(len(key) == m)
    
    #shifts
    key1 = [ dalphabet.get(x) for x in iter(key) ]

    plaintxt = ''
    i = -1
    for x in ciphertxt:
        x = str(x)
        if x in alphabet:
            #print(x)
            i += 1
            j = divmod(i, m)[1]
            y = divmod(dalphabet.get(x) - key1[j], 26)[1]            
            #print(y, dalphabet.get(y))
            plaintxt += dalphabet.get(y).lower()
        else:
            plaintxt += x
        
    #output
    print(plaintxt)