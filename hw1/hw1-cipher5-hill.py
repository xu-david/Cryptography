#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''CIPHER 5 HILL'''

import numpy as np
import string
from itertools import zip_longest
import sympy

def grouper(iterable, n, fillvalue=''):
    #get fixed chunks, from py3 docs
    args = [ iter(iterable) ] * n
    return zip_longest(*args, fillvalue=fillvalue)

if __name__ == '__main__':
    cipherfile = 'hw1-ciphers/cipher5.txt'
    
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
    
    plaintext = 'shesellsseashellsbytheseashoretheshellsshesellsaresurelysea\
shellssoifshesellsshellsontheseashoreimsureshesellsseashoreshells'
    print(cipherstrj, plaintext, sep='\n')
    
    #solve
    m = 2
    lptxt = [ x for x in grouper(plaintext, pow(m, 2)) ]
    lctxt = [ y for y in grouper(cipherstrj, pow(m, 2)) ]
    
    for ptxt, ctxt in zip(lptxt, lctxt):
        print(ptxt, ctxt)
        #matrix Y = XK, K = X^-1 Y
        mx = np.array([dalphabet.get(x.upper()) for x in ptxt]).reshape((m, m))
        my = np.array([dalphabet.get(x) for x in ctxt]).reshape((m, m))

        mx1 = sympy.Matrix(mx)
        my1 = sympy.Matrix(my)
        
        print('x', mx1)
        print('y', my1)
        
        #inv_mod
        try:
            mx1inv = mx1.inv_mod(26)
        except ValueError:
            print('no mod inverse')
            print('-' * 10)
            continue
        print('x inverse', mx1inv)
        
        k = mx1inv * my1
        k1 = sympy.Matrix(np.array(k) % 26)
        
        print('k', k1)
        
        kinv = k.inv_mod(26)
        print('k inverse', kinv)
        
        
        print('-' * 10)
        