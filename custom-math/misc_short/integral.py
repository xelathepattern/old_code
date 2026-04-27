# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 19:23:49 2021

@author: Xela
"""


from numpy import arange

from decimal import Decimal
from decimal import getcontext

import matplotlib.pyplot as plt

from math import sin, cos, e, pi

from tqdm import tqdm


def lram(f, a, b, n, precision=None, useDecimal=True, showProgressBar=True):
   if showProgressBar==False:
      tqdm = lambda anything: anything #disables tqdm by making it do nothing.
   if useDecimal:
      if precision:
         getcontext().prec = precision
   
   
      a = Decimal(str(a))
      b = Decimal(str(b))
   
      area = 0
      deltaX = (b-a)/n
      for i in tqdm(range(n)):
         area += (Decimal(str(f(a + i*deltaX)))*deltaX)

   else:
      area = 0
      deltaX = (b-a)/n
      for i in tqdm(range(n)):
         area += (f(a + i*deltaX)*deltaX)


   return area

bounds = [ [-10,10,.1], [-10,10,.1] ]


def antiderivative(f, point, n, bounds=bounds, precision=None): #bounds: [ [xLow, xHigh, xStep], [yLow, yHigh, yStep] ]
   if precision:
      getcontext().prec = precision

   xVals = arange(bounds[0][0], bounds[0][1], bounds[0][2])

   F = lambda x: lram(f, point[0], x, n) + point[1]

   yVals = []
   forwardYVals = []
   for x in tqdm(xVals):
      yVals.append(Decimal(str(F(Decimal(str(x))))))
      forwardYVals.append(Decimal(str(f(Decimal(str(x))))))


   ax = plt.subplot() #create the plot, get the figure elements

   plt.axis(bounds[0][0:2] + bounds[1][0:2])

   plt.plot(xVals, yVals)

   plt.plot(xVals, forwardYVals)

   ax.grid(True, which='both')

   ax.axhline(y=0, color='k')
   ax.axvline(x=0, color='k')


   return F


def f(x):
   return (Decimal('1')+(Decimal(str(cos(x))))**Decimal('2'))**Decimal('.5')