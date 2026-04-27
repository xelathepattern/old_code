# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:33:33 2021

@author: Xela
"""


from problem7 import primeTest

from tqdm import tqdm


def primeListUnderN(n):
   primes = []
   for i in tqdm(range(2, n)):
      if primeTest(i, possiblePrimes=primes, showProgressBar=False):
         primes.append(i)


   return primes