# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:15:45 2021

@author: Xela
"""


import sympy
from sympy import Matrix


def makeVercombeMatrix(n):
   outMatrix = []
   for x_i in range(1,n+1):
      outMatrix.append([x_i**j for j in range(n)])


   return Matrix(outMatrix)


def actualSumOfSquares(n):
   return sum([i**2 for i in range(1, n+1)])


def interpolateSumOfSquares(n):
   vercombeMatrix = makeVercombeMatrix(n)
   augmentedMatrix = vercombeMatrix.col_insert(len(vercombeMatrix), Matrix([ [actualSumOfSquares(n)] for n in range(1,n+1) ]) )

   rrefAugmentedMatrix = augmentedMatrix.rref()[0]

   #the last column should be [0,1/6,1/2,1/3,0,0,...]

   return rrefAugmentedMatrix.col(-1)