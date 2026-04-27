# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 13:21:43 2022

@author: Xela
"""


import matplotlib.pyplot as plt


def coconutsAfterNextPirate(prevN, numOfPirates=5):
    return (prevN-1)*((numOfPirates-1)/numOfPirates)

def checkNum(nStart, numOfPirates=5, endingResidue=0):
    ns = [nStart]
    for i in range(numOfPirates):
        nextN = coconutsAfterNextPirate(ns[-1], numOfPirates=numOfPirates)
        if nextN <= 0 or not nextN.is_integer():
            return False
        else:
            ns.append(nextN)

    if not ns[-1]%numOfPirates == endingResidue:
        return False
    else:
        return True


n = 1
valid = []
while True:
    if n % 10000 == 0:
        print(f"Progress: {n}")
    if checkNum(n):
        valid.append(n)
        print(f"Solution: {n}")

    n += 1
