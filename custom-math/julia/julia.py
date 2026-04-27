# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 23:15:16 2021

@author: Xela
"""


j = (-1)**.5

from mpmath import e, pi


from mpmath import mp, mpf, mpc

from mpmath import arange

from tqdm.contrib.itertools import product as cartProduct


import matplotlib.pyplot as plt

from decimal import Decimal #only used to prevent hissy fits


from tqdm import tqdm


from joblib import Parallel, delayed


from imageio import imread, mimsave

from datetime import datetime



def plotSet(pointSet, window=None, adaptiveMarker=False):
   pointList = list(pointSet)

   realList = [point.real for point in pointList]
   imagList = [point.imag for point in pointList]

   if not window:
      rectangularMarker = [(-1,-1),(-1,1),(1,1),(1,-1)]
   else:
      xPointsLength, yPointsLength = len(arange(*window[0])) - 1, len(arange(*window[1])) - 1

      aspectRatio = xPointsLength/yPointsLength

      markerLength = (1/xPointsLength) * abs(window[0][1]-window[0][0])

      #if the length of the rectangle = 1, the height = aspectRatio (this rectangle is used because it has the same aspect ratio as the window)
      rectangularMarker = [ (-markerLength*mpf('.5'), -aspectRatio*markerLength*mpf('.5')), (-markerLength*mpf('.5'), aspectRatio*markerLength*mpf('.5')), (markerLength*mpf('.5'), aspectRatio*markerLength*mpf('.5')), (markerLength*mpf('.5'), -aspectRatio*markerLength*mpf('.5')) ]




   fig, ax = plt.subplots()
   if adaptiveMarker:
      ax.plot(realList, imagList, '.', marker=rectangularMarker, markersize=1)
   else:
      ax.plot(realList, imagList, '.', markersize=1)


   if window:
      #convert to Decimal so matplotlib doesn't throw a hissy fit
      ax.set_xlim([Decimal(str(window[0][0])), Decimal(str(window[0][1]))])
      ax.set_ylim([Decimal(str(window[1][0])), Decimal(str(window[1][1]))])


   return fig,ax


def julia(f, window, iters, precision, boundLimit, barToggle=True): #returns the julia set (technically, the filled-in julia set) of a function within a window (window = [ [xMin, xMax, xStep], [yMin, yMax, yStep] ])
   mp.dps = precision

   pointSet = set({})
   for coord in cartProduct(arange(*window[0]), arange(*window[1]), tqdm_class=tqdm, disable=(not barToggle)):
      a,b = coord

      pastZ = (f(mpc(str(a), str(b))))
      exceedBoundLimit = False
      for i in range(iters):
         currentZ = f(pastZ)
         if abs(currentZ) > boundLimit:
            exceedBoundLimit = True

            break

         else:
            pastZ = currentZ


      if not exceedBoundLimit:
         pointSet.add(mpc(str(a), str(b)))


   return plotSet(pointSet, window)



def juliaAsync(f, window, iters, precision, boundLimit, barToggle=True): #slower than julia()
   mp.dps = precision

   pointSet = set({})

   def checkCoord(coord):
      a,b = coord

      pastZ = (f(mpc(str(a), str(b))))
      exceedBoundLimit = False
      for i in range(iters):
         currentZ = f(pastZ)
         if abs(currentZ) > boundLimit:
            exceedBoundLimit = True

            break

         else:
            pastZ = currentZ


      if not exceedBoundLimit:
         pointSet.add(mpc(str(a), str(b)))


   Parallel(n_jobs=8, require='sharedmem')(delayed(checkCoord)(coord) for coord in cartProduct(arange(*window[0]), arange(*window[1]), tqdm_class=tqdm, disable=(not barToggle)))


   return plotSet(pointSet, window)


def juliaSweep(f, window, iters, precision, boundLimit, cRange): #f is a function of c and z, and returns the julia sets for each [f(z,c) where c is constant] for all values of c in the cRange
   cRange = arange(*cRange)

   for c in tqdm(cRange): #curry f
      curriedF = lambda z: f(z, c)

      plt.figure()
      fig, ax = julia(curriedF, window, iters, precision, boundLimit, barToggle=False)

      ax.set_title('c = %s' % c)


      fig.savefig('plots\\julia\\frames\\%s.png' % c)
      plt.close(fig)


   images = []
   for c in cRange:
      images.append(imread('plots\\julia\\frames\\%s.png' % c))


   timestamp = str(datetime.now()).replace(':', '-').replace('.', '-')

   mimsave('plots\\julia\\julia %s.mp4' % timestamp, images, quality=7)


def juliaSweepAsync(f, window, iters, precision, boundLimit, cRange): #not to be confused with the potential juliaAsyncSweep
   cRange = arange(*cRange)

   def getPlot(c):
      curriedF = lambda z: f(z, c)

      fig, ax = julia(curriedF, window, iters, precision, boundLimit, barToggle=False)

      ax.set_title('c = %s' % c)


      fig.savefig('plots\\julia\\frames\\%s.png' % c)
      plt.close(fig)


   Parallel(n_jobs=8, require='sharedmem')(delayed(getPlot)(c) for c in tqdm(cRange))


   images = []
   for c in cRange:
      images.append(imread('plots\\julia\\frames\\%s.png' % c))


   timestamp = str(datetime.now()).replace(':', '-').replace('.', '-')

   mimsave('plots\\julia\\julia %s.mp4' % timestamp, images, quality=7)


def f(z,c):
    return z**2 + mpf('.7885')*e**(mpc(real=0,imag=1)*c)



def mandelbrot(window, iters, precision, boundLimit=2, d=2, barToggle=True):
   mp.dps = precision

   pointSet = set({})
   for coord in cartProduct(arange(*window[0]), arange(*window[1]), tqdm_class=tqdm, disable=(not barToggle)):
      a,b = coord

      pastZ = 0
      exceedBoundLimit = False
      for i in range(iters):
         currentZ = pastZ**d + mpc(str(a), str(b))
         if abs(currentZ) > boundLimit:
            exceedBoundLimit = True

            break

         else:
            pastZ = currentZ


      if not exceedBoundLimit:
         pointSet.add(mpc(str(a), str(b)))


   return plotSet(pointSet, window)


def multibrotSweep(window, iters, precision, dRange, boundLimit=2, asyncToggle=True):
   dRange = arange(*dRange)

   def getPlot(d):
      fig, ax = mandelbrot( window, iters, precision, boundLimit=boundLimit, d=d, barToggle=False)

      ax.set_title('d = %s' % d)


      fig.savefig('plots\\multibrot\\frames\\%s.png' % d)
      plt.close(fig)


   if asyncToggle:
      _=Parallel(n_jobs=8, require='sharedmem')(delayed(getPlot)(d) for d in tqdm(dRange))
   else:
      _=[getPlot(d) for d in tqdm(dRange)]


   images = []
   for d in dRange:
      images.append(imread('plots\\multibrot\\frames\\%s.png' % d))


   timestamp = str(datetime.now()).replace(':', '-').replace('.', '-')

   mimsave('plots\\multibrot\\multibrot %s.mp4' % timestamp, images, quality=7)



window=[[mpf(-2),mpf(1),mpf('.009')],[mpf(-1.5),mpf(1.5),mpf('.009')]]
iters=50
precision=5
boundLimit=2

#juliaSweepAsync(f, window, iters, precision, boundLimit, [0,2*pi,.1])
multibrotSweep(window, iters, precision, [0, 3, .1], asyncToggle=True)
