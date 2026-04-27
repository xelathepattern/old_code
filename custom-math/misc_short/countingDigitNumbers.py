# -*- coding: utf-8 -*-
"""
Created on Wed May  4 12:36:48 2022

@author: Xela 
"""


import itertools
import functools
import math

import matplotlib.pyplot as plt

from tqdm import tqdm

DIGITS = {0,1,2,3,4,5,6,7,8,9}

def bruteCount(numOfDigits, targetDigit=9):
    return len(tuple(filter(lambda numTuple: targetDigit in numTuple, itertools.product(*([list(DIGITS)]*(numOfDigits))))))

def closedCount(numOfDigits):
    return int(sum([ ((-1)**(i+1))  * (math.factorial(numOfDigits) / (math.factorial(i)*math.factorial(numOfDigits-i)) ) * (len(DIGITS)**(numOfDigits-i)) for i in range(1, numOfDigits+1) ]))

def closedProp(numOfDigits):
    return closedCount(numOfDigits)/(len(DIGITS)**numOfDigits)

def fastClosedProp(numOfDigits):
    return sum([ ((-1)**(i+1))  * (math.factorial(numOfDigits) / (math.factorial(i)*math.factorial(numOfDigits-i)) ) * (len(DIGITS)**(-i)) for i in range(1, numOfDigits+1) ])

def checkInterval(start, end):
    return all([bruteCount(i)==closedCount(i) for i in tqdm(range(start, end))])

plt.plot(list(range(100)), [fastClosedProp(n) for n in range(100)])
