#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''CIPHER 3 SUBSTITUTION'''

import string
import re
from collections import Counter
from itertools import islice

def sliding_window(seq, n):
    it = iter(seq)
    r = tuple(islice(it, n))
    if len(r) == n:
        yield r
    for e in it:
        r = r[1:] + (e,)
        yield r

if __name__ == '__main__':
    cipherfile = 'hw1-ciphers/cipher3.txt'
    
    with open(cipherfile) as f:
        lines = [ x for x in f.readlines() ]
        ciphertxt = ''.join(lines)

    #no punctuation
    alphabet = string.ascii_uppercase
    cipherstr = [ x for x in iter(ciphertxt) if x in alphabet]
    
    #check letter frequency
    print('single letter freq')
    for k, v in sorted(Counter(cipherstr).items(), key=lambda x: x[1], reverse=1):
        print(k, v, v/len(cipherstr))
    print('-'*10)
    
    #check n-letter frequency
    rgx = re.compile("(\w[\w']*\w|\w)")
    for n in range(2, 4):
        l = []
        for word in rgx.findall(ciphertxt):
            for s in sliding_window(word, n):
                l.append(s)
        
        print('{}-gram freq'.format(n))
        for c, (k, v) in enumerate(sorted(Counter(l).items(), key=lambda x: x[1], reverse=1)):
            if c >= 20:
                break
            print(k, v, v/len(cipherstr))
        print('-'*10)
    
    #guess some letters
    dmap = {}
    dmap['Z'] = 't'
    dmap['I'] = 'h'
    dmap['T'] = 'e'
    dmap['Q'] = 'a'
    dmap['F'] = 'n'
    dmap['R'] = 'd'
    dmap['O'] = 'i'
    dmap['L'] = 's'
    dmap['V'] = 'w'
    dmap['K'] = 'r'
    dmap['G'] = 'o'
    dmap['X'] = 'u'
    dmap['W'] = 'b'
    dmap['E'] = 'c'
    dmap['H'] = 'p'
    dmap['Y'] = 'f'
    dmap['D'] = 'm'
    dmap['S'] = 'l'
    dmap['U'] = 'g'
    dmap['N'] = 'y'
    dmap['J'] = 'q'
    dmap['C'] = 'v'
    dmap['B'] = 'x'
    dmap['A'] = 'k'
    dmap['P'] = 'j'
    dmap['M'] = 'z'
    
    #check unmapped
    unusedc = [ k for k in alphabet if k not in dmap ]
    unusedp = [ k.lower() for k in alphabet if k.lower() not in dmap.values() ]
    print('unmapped CRYPTKEYS', unusedc)
    print('unmapped plaintext', unusedp)
    print('-' * 10)
    
    for k, v in dmap.items():
        ciphertxt = ciphertxt.replace(k, v)
    
    #output
    print(ciphertxt)