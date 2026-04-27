# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:19:16 2022

@author: xela 
"""


import matplotlib.pyplot as plt

import seaborn as sb

import numpy as np

from tqdm import tqdm


def gradAtPoint(f, x, y, dx, dy):
    return [( f(x+dx/2, y) - f(x-dx/2,y) )/dx, ( f(x, y+dy/2) - f(x,y-dy/2) )/dy]

def divAtPoint(f, x, y, dx, dy):
    xComp = (f(x+dx/2, y)[0] - f(x-dx/2,y)[0])/dx
    yComp = (f(x, y+dy/2)[1] - f(x,y-dy/2)[1])/dy

    return xComp + yComp

grad = lambda f, dx, dy: (lambda x,y: gradAtPoint(f, x, y, dx, dy))
div = lambda f, dx, dy: (lambda x,y: divAtPoint(f, x, y, dx, dy))

def lap(f, dx, dy):
    return div(grad(f,dx,dy),dx,dy)

def plotScalarValued(f, xCoords, yCoords, heatLims, cmap='inferno'):
    data = []
    for y in yCoords:
        row = []
        for x in xCoords:
            row.append(f(x,y))

        data.append(row)

    fig, ax = plt.subplots()
    sb.heatmap(data, ax=ax, vmin=heatLims[0], vmax=heatLims[1], cmap=cmap)

    xLabels = np.arange(xCoords[0], xCoords[-1], (xCoords[-1]-xCoords[0])/len(xCoords))
    yLabels = list(np.arange(yCoords[0], yCoords[-1], (yCoords[-1]-yCoords[0])/len(yCoords)))
    yLabels.reverse()
    #print(xLabels)
    xStepAmount = len(xLabels)//10
    yStepAmount = len(yLabels)//10

    roundedXLabels = [] #round to prevent the floating point errors from creating a completely unreadable label
    for x in xLabels[::xStepAmount]:
        roundedXLabels.append(round(x, 2))

    roundedYLabels = []
    for y in yLabels[::yStepAmount]:
        roundedYLabels.append(round(y, 2))

    xTickLocs = range(len(xLabels))[::xStepAmount]
    yTickLocs = range(len(yLabels))[::yStepAmount]

    #print(xTickLocs, roundedXLabels)
    plt.xticks(xTickLocs, roundedXLabels)
    plt.yticks(yTickLocs, roundedYLabels)

    return fig

def distance(a, b):
    return (a[0]**2 + b[0]**2)**.5

def solve(initialState, xCoords, yCoords, tLims, dx, dy, dt, boundaryDistance=.01): #!!! boundary conditions
    stateList = [initialState]
    t = tLims[0]
    i = 1
    for t in tqdm(np.arange(*tLims, dt)):
        #from the docs.python.org faq: without using i=i, when i is incremented the value of i inside of the lambda will also be incremented because the i is only accessed at eval time - setting i=i will evaluate i and set it as the default value, so that the lambda actually stores the i value that it should have
        def currentState(x,y,i=i, ignoreBoundary=False):
            x0Dist, x1Dist, y0Dist, y1Dist = abs(x - (xCoords[0]+boundaryDistance)), abs(x - (xCoords[-1]-boundaryDistance)), abs(y-(yCoords[0]+boundaryDistance)), abs(y-(yCoords[-1]-boundaryDistance))
            distance = min([x0Dist, x1Dist, y0Dist, y1Dist])
            #else: #not on boundary
            #    print('no boundary')
            #    return stateList[i-1](x,y) + lap(stateList[i-1], dx, dy)(x,y)*dt

            onBoundary = False
            if distance < boundaryDistance:
                onBoundary = True

            if onBoundary and ignoreBoundary==False:
                #!!!actually do stuff
                return stateList[i-1](x,y) + lap(stateList[i-1], dx, dy)(x,y)*dt
            else:
                return stateList[i-1](x,y) + lap(stateList[i-1], dx, dy)(x,y)*dt


        stateList.append(currentState)

        i+=1

    return stateList


def initialFunc(x,y,ignoreBoundary=False): #for initialFunc, ignoreBoundary is just there to stop errors when using it
    return -(x**2+y**2)+5


def main():
    solved = solve(initialFunc, xCoords, yCoords, tLims, dx, dy, dt)
    figs = map(lambda stateFunc: plotScalarValued(stateFunc, xCoords, yCoords, heatLims), solved)
    with tqdm(total=len(np.arange(*tLims,dt))) as pbar:
        for fig in figs:
            fig.show()
            pbar.update(1)

    return solved, figs

xCoords = np.arange(-1, 1, .01)
yCoords = np.arange(-1, 1, .01)
tLims = [0, 2]
heatLims = [3,5]
dx, dy, dt = .01, .01, .1

solved, figs = main()
#plotScalarValued(laplacian(f,dx, dy), xCoords, yCoords, heatlims, cmap='viridis')
