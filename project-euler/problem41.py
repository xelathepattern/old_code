# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 11:34:06 2021

@author: Xela
"""


from problem7 import primeTest

from collections import Counter

from itertools import permutations


def pandigitalTest(n):
   nDigits = len(str(n))
   digitCounts = Counter(str(n))
   for i in range(1,nDigits+1):
      if digitCounts[str(i)] != 1:
         return False

   return True


def solve():
   pandigitalPrimes = []
   for iAsList in permutations('1234567'):
      iAsString = ''
      for char in iAsList:
         iAsString += char

      i = int(iAsString)

      if primeTest(i, showProgressBar=False):
         pandigitalPrimes.append(i)


   return max(pandigitalPrimes)