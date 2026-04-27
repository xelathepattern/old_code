# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 00:40:57 2021

@author: Xela
"""


from collections import Counter
from decimal import Decimal


def primeFactorize(n, isRecursed=False):
   factorTestLimit = int(Decimal(n)**Decimal('.5')) #if no factors up to sqrt(n), then n is prime

   primeFactors = []
   prime = True
   for i in range(2, factorTestLimit + 1):
      if not(n%i):
         prime = False

         primeFactors += primeFactorize(i, isRecursed=True)

         primeFactors += primeFactorize(n//i, isRecursed=True)


         break


   if prime:
      return [n]
   else:
      if not isRecursed:
         return Counter(primeFactors)
      else:
         return primeFactors