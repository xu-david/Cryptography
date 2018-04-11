#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''CIPHER 4 LFSR4'''

import numpy as np
import string
from itertools import islice, zip_longest
import sympy

def sliding_window(seq, n):
    #generator function for sliding window given sequence and n
    it = iter(seq)
    r = tuple(islice(it, n))
    if len(r) == n:
        yield r
    for e in it:
        r = r[1:] + (e,)
        yield r

def grouper(iterable, n, fillvalue=''):
    #get fixed chunks from some iterable, from py3 docs
    args = [ iter(iterable) ] * n
    return zip_longest(*args, fillvalue=fillvalue)

def find_lfsr(x, m):
    #find inverse matrix
    #(c_0 ... c_m-1) = (z_m+1, z_2m) (z1 ... zm ... z_2m squared matrix)
    meq = []
    for y in sliding_window(x[:-1], m):
        meq.append(y)
    
    #print(meq)
    try:
        meq = sympy.Matrix(meq)
        #print(meq)
        meqinv = meq.inv_mod(26)
    except:
        #print('no inv matrix')
        #print('-' * 10)
        return 0, []

    meqinv = np.array(meqinv)
    #print('inverse matrix', meqinv)
    
    mz = np.array(x[m:]).reshape(1, m)
    
    #print(mz)
    print(np.dot(mz, meqinv) % 26)
    return 1, meqinv

def find_z(guessctxt, guessptxt, dalphabet):
    #returns list of z elements from cipher and plaintext in mod 26
    guessc = [ dalphabet.get(x) for x in iter(guessctxt)]
    guessp = [ dalphabet.get(x.upper()) for x in iter(guessptxt)]
    #z = ( c - p ) mod 26
    #print('Y', guessc)
    #print('X', guessp)
    guessz = []
    for i in range(len(guessc)):
        guessz.append(divmod(guessc[i] - guessp[i], 26)[1])
    #print('Z', guessz)
    return guessz
    
if __name__ == '__main__':
    cipherfile = 'hw1-ciphers/cipher4.txt'
    
    with open(cipherfile) as f:
        lines = [ x for x in f.readlines() ]
        ciphertxt = ''.join(lines)

    #initialize some stuff
    alphabet = string.ascii_uppercase
    cipherstr = [ x for x in iter(ciphertxt) if x in alphabet]
    cipherstrj = ''.join(cipherstr)
    
    dalphabet = { i:j for i,j in enumerate(alphabet) }
    for i in list(dalphabet.keys()):
        dalphabet[dalphabet[i]] = i

    m = 4

    #guess probable cipher string?
    
    #   QJ ZVO 70'I. XVI 70'A SEZI
    #   in the 70's. the 70's were
    #guessctxt = 'QJZVOIXVIASEZI'
    #guessptxt = 'inthestheswere'
    #guessptxt = 'bythestheswere'
    
    guessctxt = 'ZVOIXVIA'
    guessptxt = 'thesthes'
    
    #   ZXA  70'U FCJ BDQ 60'M
    #   the  70's and the 60's
    #guessctxt = 'UFCJBDQM'
    #guessptxt = 'sandthes'
    #guessptxt = 'sbutthes'
    #guessptxt = 'sbutnots'
    #guessptxt = 'sandnots'
    #guessptxt = 'snotthes'
    
    #  49% YB TRK CENNV'G FWLGFQVEAB. 49% YB DBU WIBVH'G NQFIBGNSEX
    #  49% of the world's population. 49% of the World's population
    #guessctxt = 'YBTRKCENNVGFWLGFQVEABYBDBUWIBVHGNQFIBGNSEX'
    #guessptxt = 'oftheworldspopulationoftheworldspopulation'
    
    #WN 1066. AADHWGO JDC QYVMASBUV WRDWDMH IZWFGJT EF 1066. EMHPQEU JBG UABWMKDIB
    #in 1066. william the conqueror invaded England in 1066. william the conqueror
    guessctxt = 'WNAADHWGOJDCQYVMASBUVWRDWDMHIZWFGJTEFEMHPQEUJBGUABWMKDIB'
    guessptxt = 'inwilliamtheconquerorinvadedenglandinwilliamtheconqueror'

    
    guessz = find_z(guessctxt, guessptxt, dalphabet)
    
    #implement sliding window for longer guesses
    for x in sliding_window(guessz, m*2):
        print(x)
        flfsr, mzinv = find_lfsr(x, m)
        if flfsr:
            print(x, mzinv)
            print('-' * 10)