# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 12:45:55 2022

@author: Xela
"""


import traceback
import warnings
import datetime


import scipy
import scipy.integrate as integrate
import numpy as np

def complex_quadrature(func, a, b, **kwargs): #taken from stack overflow
    def real_func(x):
        return np.real(func(x))
    def imag_func(x):
        return np.imag(func(x))
    real_integral = integrate.quad(real_func, a, b, **kwargs)
    imag_integral = integrate.quad(imag_func, a, b, **kwargs)
    return (real_integral[0] + 1j*imag_integral[0], real_integral[1:], imag_integral[1:])

import math

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use("Agg")


from tqdm import tqdm

import mouse
from time import sleep
import bezier

import pickle



def warn_with_traceback(message, category, filename, lineno, file=None, line=None):

    log = file if hasattr(file,'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))

warnings.showwarning = warn_with_traceback


def sinIntegrand(f, period, fundamentalPeriod):
   return lambda x: f(x)*math.sin( (period*(2*math.pi)/fundamentalPeriod)*x )


def sinIndivFunc(period, fundamentalPeriod):
   return lambda x: math.sin( (period*(2*math.pi)/fundamentalPeriod)*x )


def cosIntegrand(f, period, fundamentalPeriod):
   return lambda x: f(x)*math.cos( (period*(2*math.pi)/fundamentalPeriod)*x )


def cosIndivFunc(period, fundamentalPeriod):
   return lambda x: math.cos( (period*(2*math.pi)/fundamentalPeriod)*x )


def fourierReal(f, limits, numberOfCoeffs=50, plotFourier=False, plotIndiv=False):
   fundamentalPeriod = limits[1]-limits[0]

   sinCoeffs = [(2/fundamentalPeriod)*integrate.quad(sinIntegrand(f, n, fundamentalPeriod), limits[0], limits[1])[0] for n in range(1,numberOfCoeffs)]
   sinSeries = lambda x: [sinCoeffs[n-1] * sinIndivFunc(n, fundamentalPeriod)(x) for n in range(1,numberOfCoeffs)]

   cosCoeffs = [(2/fundamentalPeriod)*integrate.quad(cosIntegrand(f, n, fundamentalPeriod), limits[0], limits[1])[0] for n in range(1,numberOfCoeffs)]
   cosSeries = lambda x: [cosCoeffs[n-1] * cosIndivFunc(n, fundamentalPeriod)(x) for n in range(1,numberOfCoeffs)]

   constantTerm = (1/fundamentalPeriod)*integrate.quad(f,limits[0],limits[1])[0]


   fourierEq = lambda x:  constantTerm + sum(sinSeries(x)) + sum(cosSeries(x))

   if plotFourier:
      xVals = np.arange(limits[0],limits[1],.01)
      yVals = list(map(fourierEq, xVals))
      plt.plot(xVals, yVals)

   if plotIndiv:
      xVals = np.arange(limits[0],limits[1],.01)
      [plt.plot(xVals, list(map(lambda x: constantTerm + sinSeries(x)[n-1] + cosSeries(x)[n-1], xVals))) for n in range(1,numberOfCoeffs)]


   return fourierEq, sinCoeffs, cosCoeffs


def eIndivFunc(n, fundamentalPeriod):
   return lambda x: math.e**( 1j*( (2*math.pi*n*x)/fundamentalPeriod ) )


def eIntegrand(f, n, fundamentalPeriod):
   return lambda x: f(x)* ( math.e**( -1j*( (2*math.pi*n*x)/fundamentalPeriod ) ) )


def fourierComplex(f, varList, fundamentalPeriod=None, numberOfForwardCoeffs=50, overrideFreqs=False, realPlot=False):
   if fundamentalPeriod==None:
      fundamentalPeriod = varList[-1] - varList[0]

   if overrideFreqs:
       freqList = overrideFreqs
   else:
       freqList = range(-numberOfForwardCoeffs, numberOfForwardCoeffs+1)

   coeffs = [ (1/fundamentalPeriod)*complex_quadrature(eIntegrand(f,n,fundamentalPeriod), varList[0], varList[0]+fundamentalPeriod)[0] for n in freqList]
   fourierSequenceAtX = lambda x: [coeffs[freqList.index(n)] * eIndivFunc(n, fundamentalPeriod)(x) for n in freqList]
   fourierSeries = lambda x: sum(fourierSequenceAtX(x))

   if realPlot:
      plt.plot(varList, list(map(lambda x: fourierSeries(x).real, varList)))

   return coeffs, fourierSequenceAtX, fourierSeries



def plotComplex2D(f, paramList, windowLimits=[[-1,1],[-1,1]], trailColor='blue'):
   fig, ax = plt.subplots()

   if windowLimits != None:
       ax.set_xlim(*windowLimits[0])
       ax.set_ylim(*windowLimits[1])

   plt.plot(list(map(lambda param: f(param).real,paramList)), list(map(lambda param: f(param).imag,paramList)), '.')

   return


def plotSequenceComplex2D(fourierSequenceAtX, paramList, windowLimits=[[-1,1],[-1,1]], trailColor='blue', widthOfArrow=.01):
    fig, ax = plt.subplots()

    arrowsToDelete = []

    def init():
        ax.set_xlim(*windowLimits[0])
        ax.set_ylim(*windowLimits[1])


        return []

    def animate(i):
        nonlocal arrowsToDelete #like global, but it'll only go one scope level higher.
        for arrow in arrowsToDelete:
            arrow.remove()

        ax.set_xlim(*windowLimits[0])
        ax.set_ylim(*windowLimits[1])

        points = fourierSequenceAtX(paramList[i])
        start = [0, 0]
        arrowsToDelete = []
        for i in range(len(points)):
            point = points[i]

            """
            if i < (len(points)-1)/2: #point is negative n, get its positive n cousin
                cousinPoint = points[i + (len(points)-1)//2]

            elif i == (len(points)-1)/2: #point is n=0, cousin is itself
                cousinPoint = point

            elif i > (len(points)-1)/2: #point is positive n, get its negative cousin
                cousinPoint = points[i - (len(points)-1)//2]
            """

            displacementX = point.real
            displacementY = point.imag

            endX = start[0] + displacementX
            endY = start[1] + displacementY

            arrowReference = ax.arrow(start[0], start[1], displacementX, displacementY, width=widthOfArrow, length_includes_head=True)
            arrowReference.set_color('green')
            arrowsToDelete.append(arrowReference)


            start = [endX, endY]
        ax.scatter(*start, s=1, color=trailColor)

        return []


    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(paramList), interval=20, blit=True)
    anim.save("fourier_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".mp4", fps=24)
    #plt.plot(list(map(lambda param: f(param).real,paramList)), list(map(lambda param: f(param).imag,paramList)), '.')
    return


def getUserPathPoints(samplingRate=100):
    end = False
    def stop():
        nonlocal end
        if end == False:
            end = True

    points = []
    mouse.wait(target_types=(mouse.DOUBLE))
    while True:
        mouse.on_double_click(stop)
        if not end:
            rawPoint = mouse.get_position()
            points.append(rawPoint[0]-rawPoint[1]*1j)
            sleep(samplingRate/1000)
        elif end:
            break

    return points


def translatePoints(points, translation):
    transPoints = []
    for point in points:
        transPoints.append(point.real+translation.real + 1j*(point.imag+translation.imag))

    return transPoints


def getUserPath(samplingRate=100):
    pathPoints = getUserPathPoints(samplingRate=samplingRate)
    pathPoints = translatePoints(pathPoints, -1100+750j)
    curve = bezier.nBezierSpline(pathPoints, 1)

    return curve, pathPoints



def f(x):
   #x *= 2


   #return math.e**(1j*x)
   #return math.cos(.8*x)*math.cos(x) + 1j*math.cos(.8*x)*math.sin(x)
   pass
   #x = (x+1)%2; return abs(x-1)/(x-1) if x-1 != 0 else 0
   #return math.cos(4*math.pi*x)


def saveDrawing():
    print("draw!")
    f, pathPoints = getUserPath(samplingRate=.01)
    with open('pathPoints.PICKLE', 'wb') as fi:
        pickle.dump(pathPoints, fi)
    print("drawing stored!")

    return f


def loadDrawing():
    with open('pathPoints.PICKLE', 'rb') as fi:
        pathPoints = pickle.load(fi)
    f = bezier.nBezierSpline(pathPoints, 1)

    return f


def plotActualReal(f, limits):
    xVals = np.arange(limits[0],limits[1],limits[2])
    actualYVals = list(map(f,xVals))

    plt.plot(xVals, actualYVals)


f = loadDrawing()


#realLimits = [-3,3]
#xVals = np.arange(realLimits[0], realLimits[1], .01)
#plotActualReal(f, xVals)
#fourierReal(f, xVals, numberOfCoeffs=5, plotFourier=True, plotIndiv=True)


paramLims = [0, 1]
paramList = np.arange(paramLims[0], paramLims[1], .001)
windowLims = [ [-1100, 1100], [-750, 750] ]
_, fourierSequenceAtX, fourierSeries = fourierComplex(f, paramList, numberOfForwardCoeffs=10, realPlot=False)

#plotComplex2D(f, paramList, windowLimits=windowLims)
plotSequenceComplex2D(fourierSequenceAtX, paramList, windowLimits=windowLims,  widthOfArrow=10)
