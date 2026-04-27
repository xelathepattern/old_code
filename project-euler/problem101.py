# -*- coding: utf-8 -*-
"""
Created on Wed Jun 9 21:07:20 2021

@author: Xela
"""


import sys
custom_math_path = ""
sys.path.insert(1, custom_math_path)

from polyFit import polyFit


def findFIT(OP, truePoly, truePolyOrder): #FIT = FirstIncorrectTerm, as opposed to fit, which is just the normal english definition
   trueY = truePoly(1)
   testY = OP(1)
   i = 1
   while testY == trueY:
      if i > (truePolyOrder + 1):
         return False

      trueY = truePoly(i)
      testY = OP(i)


      i += 1


   return testY


truePoly = lambda n: 1 - n + n**2 - n**3 + n**4 - n**5 + n**6 - n**7 + n**8 - n**9 + n**10
def solve(truePoly, truePolyOrder):
   FITsum = 0
   for i in range(truePolyOrder + 1):
      points = {}
      for j in range(1, i + 2):
         points[j] = truePoly(j)

      OP = polyFit(points)[0]

      FIT = findFIT(OP, truePoly, truePolyOrder)

      if not FIT:
         return FITsum
      else:
         FITsum += FIT
