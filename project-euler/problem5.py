# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 09:22:30 2021

@author: Xela
"""


from problem3 import primeFactorize

from collections import Counter


def LCM(nList):
   primes = set({})
   counts = []
   for n in nList:
      primeFactors = primeFactorize(n)

      [primes.add(prime) for prime in primeFactors]

      counts.append(Counter(primeFactors))


   primeCounts = {}
   for prime in primes:
      thisPrimeCounts = [count[prime] for count in counts]

      primeCounts[prime] = max(thisPrimeCounts)


   out = 1
   for prime in primeCounts.keys():
      out *= (prime ** primeCounts[prime])


   return out