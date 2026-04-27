# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:36:20 2021

@author: Xela
"""


n_Previous = 1
n = 2
fibList = []
while n <= 4e6:
   if n%2 == 0:
      fibList.append(n)

   newN_Previous = n
   n = n_Previous + n
   n_Previous = newN_Previous


out = sum(fibList)