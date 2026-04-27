# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 17:35:33 2021

@author: Xela
"""


#import


from collections import Counter
from decimal import Decimal
from tqdm import tqdm


def primeTest(n, showProgressBar=True, possiblePrimes=None):
   factorTestLimit = int(n**.5)

   if possiblePrimes:
      if showProgressBar:
         for i in tqdm(possiblePrimes):
            if i < (factorTestLimit + 1):
               if not(n%i):
                  return False

            else:
               break

      else:
         for i in possiblePrimes:
            if i < (factorTestLimit + 1):
               if not(n%i):
                  return False

            else:
               break



      return True

   else:
      if showProgressBar:
         for i in tqdm(range(2, factorTestLimit + 1)):
            if not(n%i):
               return False

      else:
         for i in range(2, factorTestLimit + 1):
            if not(n%i):
               return False


      return True


def nthPrimeList(n):
   i = 2
   primes = []
   pbar = tqdm(total=n)
   while len(primes) < n:
      if primeTest(i, showProgressBar=False, possiblePrimes=primes):
         primes.append(i)
         pbar.update()


      i += 1


   return primes


def primeFactorize(n, isRecursed=False, showProgressBar=True):
   factorTestLimit = int(Decimal(n)**Decimal('.5')) #if no factors up to sqrt(n), then n is prime

   primeFactors = []
   prime = True
   if showProgressBar:
      for i in tqdm(range(2, factorTestLimit + 1)):
         if not(n%i):
            prime = False

            primeFactors += primeFactorize(i, isRecursed=True, showProgressBar=True)

            primeFactors += primeFactorize(n//i, isRecursed=True, showProgressBar=True)


            break

   else:
      for i in range(2, factorTestLimit + 1):
         if not(n%i):
            prime = False

            primeFactors += primeFactorize(i, isRecursed=True, showProgressBar=False)

            primeFactors += primeFactorize(n//i, isRecursed=True, showProgressBar=False)


            break


   if prime:
      return Counter([n])
   else:
      if not isRecursed:
         return Counter(primeFactors)
      else:
         return primeFactors


def primeListUnderN(n):
   primes = []
   for i in tqdm(range(2, n)):
      if primeTest(i, possiblePrimes=primes, showProgressBar=False):
         primes.append(i)


   return primes