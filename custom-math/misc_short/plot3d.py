# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 11:53:11 2021

@author: Xela
"""


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import arange, array
from itertools import product


def f(x, y):
   return x**2

bounds = [ [-10,10,.1], [-10,10,.1] ]

def plot3dFunction(f, bounds=bounds, labels=['x','y','z']):
   xRange = arange(*bounds[0])
   yRange = arange(*bounds[1])

   xyRange = product(xRange, yRange)

   points = []
   for xy in xyRange:
      points.append(xy + tuple([f(*xy)]))

   points = array(points)

   xVals = points[:, 0]
   yVals = points[:, 1]
   zVals = points[:, 2]

   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')

   ax.plot(xVals, yVals, zVals, '.')

   ax.set_xlabel(labels[0])
   ax.set_ylabel(labels[1])
   ax.set_zlabel(labels[2])


   return fig, ax


def plot3dPoints(points, labels=['x','y','z']):
   points = array(points)

   xVals = points[:, 0]
   yVals = points[:, 1]
   zVals = points[:, 2]

   fig = plt.figure()
   ax = fig.add_subplot(111, projection='3d')

   ax.plot(xVals, yVals, zVals, '.')

   ax.set_xlabel(labels[0])
   ax.set_ylabel(labels[1])
   ax.set_zlabel(labels[2])

   return fig, ax