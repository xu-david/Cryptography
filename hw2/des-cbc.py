#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class DES_CBC(object): 
    _ip = [
        57, 49, 41, 33, 25, 17,  9,  1,
        59, 51, 43, 35, 27, 19, 11,  3,
        61, 53, 45, 37, 29, 21, 13,  5,
        63, 55, 47, 39, 31, 23, 15,  7,
        56, 48, 40, 32, 24, 16,  8,  0,
        58, 50, 42, 34, 26, 18, 10,  2,
        60, 52, 44, 36, 28, 20, 12,  4,
        62, 54, 46, 38, 30, 22, 14,  6
            ]
    
    _ip_inv = [
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25,
        32,  0, 40,  8, 48, 16, 56, 24
            ]

    _e = [
        31,  0,  1,  2,  3,  4, 
         3,  4,  5,  6,  7,  8,
         7,  8,  9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31,  0
            ]

    _p = [
        15,  6, 19, 20, 28, 11, 27, 16,
         0, 14, 22, 25,  4, 17, 30,  9,
         1,  7, 23, 13, 31, 26,  2,  8,
        18, 12, 29,  5, 21, 10,  3, 24
            ]
    
    _pc1 = [
        56, 48, 40, 32, 24, 16,  8,
         0, 57, 49, 41, 33, 25, 17,
         9,  1, 58, 50, 42, 34, 26,
        18, 10,  2, 59, 51, 43, 35,
        62, 54, 46, 38, 30, 22, 14,
         6, 61, 53, 45, 37, 29, 21,
        13,  5, 60, 52, 44, 36, 28,
        20, 12,  4, 27, 19, 11,  3
        ]
    
    _pc2 = [
        13, 16, 10, 23,  0,  4,
		  2, 27, 14,  5, 20,  9,
		 22, 18, 11,  3, 25,  7,
		 15,  6, 26, 19, 12,  1,
		 40, 51, 30, 36, 46, 54,
		 29, 39, 50, 44, 32, 47,
		 43, 48, 38, 55, 33, 52,
		 45, 41, 49, 35, 28, 31
        ]
    
    _kshift = [ 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    _sbox = [
                [
                    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
                ],
                [
                    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
                ],
                [
                    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
                ],
                [
                    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
                ],
                [
                    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
                ],
                [
                    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]                
                ],
                [
                    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
                ],
                [
                    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
                ]                
            ]
    
    def __init__(self, key, iv):
        self.iv = self.hex_to_bin(iv)

        #create key schedule
        #permutate key using pc-1
        key = self.hex_to_bin(key)
        key = self.permutate(list(key), self._pc1)
        keyl = key[:28]
        keyr = key[28:]

        self.keys = []
        for i in range(16):
            #shift keys
            keyl = self._left_shift(keyl, self._kshift[i])
            keyr = self._left_shift(keyr, self._kshift[i])

            #permutate on pc-2 to 48-bits
            key = self.permutate(keyl + keyr, self._pc2)
            self.keys.append(key)
        
    def hex_to_bin(self, x, n = 64):
        '''
        Convert hexadecimal (type str) to binary (type str) of length n
        '''
        return bin(int(x, 16))[2:].zfill(n)
    
    def bin_to_hex(self, x, n = 16):
        '''
        Convert n-bit binary (type str) to hexadecimal
        '''
        return hex(int(x, 2))[2:].zfill(n)

    def xor(self, x, y):
        '''
        xor on two iterable objects x and y with equal length
        '''
        assert(len(x) == len(y))
        l = []
        for i, j in zip(x, y):
            i = int(i)
            j = int(j)
            x = i ^ j
            l.append(x)
        return l

    def _left_shift(self, l, n):
        '''
        left shift list l by n positions
        '''
        return l[n:] + l[:n]
        
    def permutate(self, d, p):
        '''
        Permutate array d with list p
        '''
        return [d[i] for i in p ]
    
    def calc_sbox(self, l):
        '''
        Calculate the sbox for 48-bit to 32-bit conversion
        '''
        sbox = ''
        for i in range(8):
            s = list(map(str, l[6*i : 6*i + 6]))
            row = int(''.join((s[0], s[-1])), 2)
            col = int(''.join(s[1:-1]), 2)
            
            #get from col and convert to 4-bits
            v = self._sbox[i][row][col]
            sbox += bin(v)[2:].zfill(4)
        return list(sbox)
        
    def decrypt(self, data):
        '''
        Decryption on 64 bits as list of integers
        '''
        #permutate with initial permutation
        data = self.permutate(data, self._ip)
        datal = data[:32]
        datar = data[32:]
        
        #16 rounds in reverse
        for i in range(15, -1, -1):
            #temp copy previous
            datar1 = datar
            
            #f function, expand R from 32-bits to 48-bit
            datar = self.permutate(datar, self._e)
            
            #xor with k_i
            l = self.xor(datar, self.keys[i])
            
            #sbox
            sbox = self.calc_sbox(l)
            
            #permutate with p to 32 bits
            sbox = self.permutate(sbox, self._p)
            
            #left xor f(right, k_i)
            datal = self.xor(datal, sbox)
            
            #swap l and r
            datal, datar = datar1, datal

        #permutate with inverse initial permutation after final rotation
        data = self.permutate(datar + datal, self._ip_inv)
        return data
    
    def hex_to_plaintext(self, s):
        '''
        Convert hex to plaintext
        '''
        for i in range(0, len(s), 2):
            j = chr(int( s[ i : i + 2 ], 16 ))
            yield j

if __name__ == '__main__':
    #read parameters and ciphertext
    keyivFile = 'ciphers-parameter-matrix/DES-key-iv.txt'
    with open(keyivFile) as f:
        key, iv = [ x.strip().split()[-1] for x in f ]
    cipherFile = 'ciphers-parameter-matrix/DES-ciphertext.txt'
    with open(cipherFile) as f:
        lctxt = [ x.strip() for x in f ]
    
    '''
    #example
    key = '84EF48BD3FAAA3A8'
    iv  = '27A1B6FCF7933158'
    lctxt = ['93A9E968CF0016E7', '3110BAF55F2DA74E', '3BE816BDBA5DF68B']
    '''
    
    des = DES_CBC(key, iv)
    
    outstr = []
    for ctxt in lctxt:
        y = des.hex_to_bin(ctxt)
        y = des.decrypt(y)
        
        x = des.xor(y, des.iv)
        #cbc assign new iv
        des.iv = des.hex_to_bin(ctxt)
        
        #output as hex
        hexout = des.bin_to_hex(''.join(map(str, x)))
        
        #convert to plaintext
        for char in des.hex_to_plaintext(hexout):
            outstr.append(char)
    
    #plaintext
    print(''.join(outstr))