# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:55:05 2021

@author: Xela
"""


n_Previous = 0
n = 1
fibList = []
i=1
while len(str(n)) != 1000:
   newN_Previous = n
   n = n_Previous + n
   n_Previous = newN_Previous

   i += 1

out = i