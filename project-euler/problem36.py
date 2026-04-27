# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 22:00:24 2021

@author: Xela
"""


def palinTest(string):
   return (string == string[::-1])


def solve():
   palinSum = 0
   for i in range(1, int(1e6)):
      if palinTest(str(i)) and palinTest(bin(i)[2:]):
         palinSum += i

   return palinSum