# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 11:44:08 2021

@author: Xela
"""


from tqdm import tqdm


def collatz(n, trackSteps=True):
   steps = 0
   while n != 1:
      if not(n%2):
         n = n//2
      else:
         n = 3*n + 1

      if trackSteps:
         steps += 1


   return steps


def solve():
   stepsList = []
   for i in tqdm(range(1, int(1e6))):
      stepsList.append(collatz(i))


   maxSteps = max(stepsList)

   maxStepsIndex = stepsList.index(maxSteps)

   maxStepsStart = maxStepsIndex + 1


   return maxStepsStart