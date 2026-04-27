# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 21:08:45 2021

@author: Xela
"""


from numpy import array

from sympy import Matrix as spMatrix


def matrixToPoly(matrix): #input should be sympy matrix

   if not isinstance(matrix, spMatrix):
      matrix = spMatrix(matrix)

   matrix = matrix.rref()[0]
   matrix = array(matrix)

   polyOrder = len(matrix)

   mList = []
   for i in list(matrix):
      mList.append(list(i))

   j = polyOrder - 1
   coefs = {}
   for i in mList:
      coefs[j] = i[-1]
      j -= 1


   poly = ''
   i = 0 #0
   while i < polyOrder:
      poly += str(coefs[i]) + '*(x**' + str(i) + ') + '
      i += 1

   poly += 'end'
   poly = poly.replace('*(x**0)', '').replace(' + end', '')

   return poly


def polyFit(points, polyOrder=None):
   if polyOrder == None:
      polyOrder = len(points)
   else:
      polyOrder += 1 #since past me thought it was a good idea for the variable polyOrder to be the order of the polynomial - 1, and since I don't want to find and fix this everywhere, this is just a quick fix.

   xVals = list(points.keys())[:polyOrder]
   matrixList = []
   j = polyOrder
   i = []
   for x in xVals:
      while j > 0:
         i.append(x**(j-1))
         j -= 1

      i.append(points[x])

      matrixList.append(i)

      i = []
      j = polyOrder

   matrix = array(matrixList)

   poly = matrixToPoly(matrix)

   f = lambda x: eval(poly)


   return f, poly