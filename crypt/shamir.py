# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 10:11:34 2020

@author: Xela
"""

#v=3.0.0


from random import randint

import numpy as np
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


def pointsToPoly(points, polyOrder=None):
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

   matrix = np.array(matrixList)

   poly = matrixToPoly(matrix)

   f = lambda x: eval(poly)


   return f, poly


def binEncode(text):
   out = '1'
   for i in text:
      out += bin(ord(i))[2:].zfill(8) #bits required for ascii

   return int(out,2)


def split(text, n):

   #inspired by stackoverflow answer
	return [text[i:i+n] for i in range(0, len(text), n)]


def binDecode(num):
   num = str(bin(num)[2:])[1:]

   out = ''
   for i in split(num, 8):
      out += chr(int(i,2))

   return out


def shamirEncode(text, minShareNum, xVals=None, shareNum=None):
   #xVals is a list of the xVals wanted
   #if none, premake default xVals
   if xVals == None:
      xVals = range(1, shareNum+1)

   codedNum = str(binEncode(text))
   polyOrder = int(minShareNum) #polyOrder n means its an n-1 order polynomial.

   #generate poly
   poly = codedNum
   i = 1
   randSize = len(codedNum)
   while i < polyOrder:
      poly += str(randint(10**randSize, 10**(randSize+1)-1)) + '*x**' + str(i) + ' + '
      i += 1
   poly += codedNum

   #turn poly into function
   def f(x):
      return eval(poly)

   #get coded points
   points = {}
   for x in xVals:
      points[x] = f(x)

   return points, poly


def shamirDecode(points, polyOrder=None): #default is for polyOrder to equal len(points)
   f, poly = pointsToPoly(points, polyOrder=polyOrder)


   return binDecode(f(0))



def test():
   return shamirDecode(shamirEncode("Hello, World!", 5, shareNum=9)[0], 4)