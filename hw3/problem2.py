# -*- coding: utf-8 -*-
"""
hw3, problem 2 ElGamal
"""

def decrypt_elgamal(y1, y2, a, p):
    #dK(y1,y2) = y2(y1^a)^-1 mod p
    #decrypt_elgamal(435, 2396, 765, 2579) = 1299
    y1ainv = modinv(pow(y1, a), p)
    #print(y1ainv)
    assert pow(y1, a) * y1ainv % p == 1 #a * a^-1 = 1 mod p
    x = y2 * y1ainv % p
    return x
    
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

def map_plaintext(s):
    #s = s1 * 26^2 + s2 * 26^1 + s3
    #2398 -> (3, 14, 6)
    #1371 -> (2, 0, 19)
    #17575 -> (25, 25, 25)
    s3 = s % 26
    s = s - s3
    s2 = s // 26 % 26
    s = s - (26 * s2)
    s1 = s // 26 // 26
    return s1, s2, s3

if __name__ == '__main__':
    #           01234567891123456789212345
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    dalphabet = { i:j for i, j in enumerate(iter(alphabet))}

    p = 31847
    alpha = 5
    a = 7899
    beta = 18074
    
    lelgamal = [
    (3781, 14409),	(31552, 3930),	(27214, 15442),	(5809, 30274),
    (5400, 31486),	(19936, 721),	(27765, 29284),	(29820, 7710),
    (31590, 26470),	(3781, 14409),	(15898, 30844),	(19048, 12914),
    (16160, 3129),	(301, 17252),	(24689, 7776),	(28856, 15720),
    (30555, 24611),	(20501, 2922),	(13659, 5015),	(5740, 31233),
    (1616, 14170),	(4294, 2307),	(2320, 29174),	(3036, 20132),
    (14130, 22010),	(25910, 19663),	(19557, 10145),	(18899, 27609),
    (26004, 25056),	(5400, 31486),	(9526, 3019),	(12962, 15189),
    (29538, 5408),	(3149, 7400),	(9396, 3058),	(27149, 20535),
    (1777, 8737),   	(26117, 14251),	(7129, 18195),	(25302, 10248),
    (23258, 3468),	(26052, 20545),	(21958, 5713),	(346, 31194),
    (8836, 25898),	(8794, 17358),	(1777, 8737),	(25038, 12483),
    (10422, 5552),	(1777, 8737),	(3780, 16360),	(11685, 133),
    (25115, 10840),	(14130, 22010),	(16081, 16414),	(28580, 20845),
    (23418, 22058),	(24139, 9580),	(173, 17075),	(2016, 18131),
    (19886, 22344),	(21600, 25505),	(27119, 19921),	(23312, 16906),
    (21563, 7891),	(28250, 21321),	(28327, 19237),	(15313, 28649),
    (24271, 8480),	(26592, 25457),	(9660, 7939),	(10267, 20623),
    (30499, 14423),	(5839, 24179),	(12846, 6598),	(9284, 27858),
    (24875, 17641),	(1777, 8737),	(18825, 19671),	(31306, 11929),
    (3576, 4630),    (26664, 27572),	(27011, 29164),	(22763, 8992),
    (3149, 7400),	    (8951, 29435),	(2059, 3977),	(16258, 30341),
    (21541, 19004),	(5865, 29526),	(10536, 6941),	(1777, 8737),
    (17561, 11884),	(2209, 6107),	(10422, 5552),	(19371, 21005),
    (26521, 5803),	(14884, 14280),	(4328, 8635),	(28250, 21321),
    (28327, 19237),	(15313, 28649),
    ]
    
    plaintext = []
    for y1, y2 in lelgamal:
        x = decrypt_elgamal(y1, y2, a, p)
        #print(y1, y2, s)
        s = map_plaintext(x)
        print(x, s)
        for i in s:
            plaintext.append(dalphabet.get(i))
    print(''.join(plaintext))