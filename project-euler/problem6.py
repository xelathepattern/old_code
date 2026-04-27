# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:28:05 2021

@author: Xela
"""

def solve():
   numSum = 0
   for i in range(1, 101):
      numSum += i

   squaredNumSum = numSum**2


   squaredSum = 0
   for i in range(1, 101):
      squaredSum += i**2


   return (squaredNumSum - squaredSum)

