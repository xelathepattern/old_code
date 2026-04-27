# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 01:28:50 2021

@author: Xela
"""


from itertools import product as cartProduct


def palinTest(n):
   return bool(str(n) == str(n)[::-1])


def solve():
   productPairs = cartProduct(range(100, 1000), range(100, 1000))

   palindromes = []
   for pair in productPairs:
      product = pair[0] * pair[1]

      if palinTest(product):
         palindromes.append(product)


   return palindromes