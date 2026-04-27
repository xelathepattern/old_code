# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 09:55:55 2021

@author: Xela
"""


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