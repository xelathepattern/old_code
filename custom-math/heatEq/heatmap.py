# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:51:53 2021

@author: Xela
"""


import math

import numpy

import matplotlib.pyplot as plt


def f(x,y):
   return math.cos( .8*(x**2 + y**2)**.5 )


def makeHeatmapArr(f, xyRange): #xyRange is [xRange, yRange] where both elements are iterables
   heatmapArr = numpy.zeros( (len(xyRange[0]), len(xyRange[1])) )
   for i in range(len(xyRange[0])):
      for j in range(len(xyRange[1])):
         heatmapArr[i,j] = f(xyRange[0][i], xyRange[1][j])


   #normally axes are jumbled, we need to flip diagonally and then flip y axis
   heatmapArr = numpy.swapaxes(heatmapArr, 0, 1)
   heatmapArr = numpy.flip(heatmapArr, 0)

   return heatmapArr


def plotHeatmapArr(f, xyRange):
   heatmapArr = makeHeatmapArr(f, xyRange)

   fig, ax = plt.subplots()

   axImage = ax.imshow(heatmapArr, extent=[xyRange[0][0], xyRange[0][-1], xyRange[1][0], xyRange[1][-1]], cmap='viridis')
   fig.colorbar(axImage, ax=ax)

   return fig, ax


#fig, ax = plotHeatmapArr(f, [numpy.arange(-10, 11, .1), numpy.arange(-10, 11, .1)] )
#fig.savefig('heatmap.svg' )
