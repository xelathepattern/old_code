# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:43:10 2021

@author: Xela
"""


def solve(numbersText):
   numbersList = numbersText.split('\r\n')

   for i in range(len(numbersList)):
      numbersList[i] = int(numbersList[i])


   return sum(numbersList)