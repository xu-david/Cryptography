#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def jacobi_symbol(m, n, s = 1):
    '''
    recursive method for jacobi symbol in form (m / n)
    '''
    #print(m, n, s)
    
    #base cases
    if m == 1:
        return 1
    elif m % n == 0:
        return 0

    #property 1
    if m % n != m:
        return jacobi_symbol(m % n, n, s)

    #property 2
    elif m == 2:
        if n % 8 in (1, 7):
            return s
        elif n % 8 in (3, 5):
            return -s

    #property 3
    elif m % 2 == 0:
        return jacobi_symbol(2, n) * jacobi_symbol(m // 2, n, s)

    #property 4
    elif m % 4 == n % 4 == 3:
        return jacobi_symbol(n, m, -s)
    else:
        return jacobi_symbol(n, m, s)
    

if __name__ == '__main__':
    for (m, n) in [
            #book example
            #(7411, 9283), # -1
            
            ##wiki examples
            #(1001, 9907), # -1
            #(19, 45), # 1
            
            #hw2
            (136, 457),
            (34333, 532789),
            (467827, 112233441),
            ]:
        s = jacobi_symbol(m, n)
        print('\t'.join(map(str, (m, n, s))))