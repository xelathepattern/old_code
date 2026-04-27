# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 08:01:56 2021

@author: Xela
"""


from copy import deepcopy
import math
from math import pi, e, sin, cos, tan

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation

import numpy as np
from numpy import array


def scalarPlot3D():
    pass


def solve(startTime, endTime, timestep, initialState, deepestDerivUpdater):
   #deepestDerivUpdater is a function of t, currentState and returns the deepest deriv of each variable
   #states are listed in reverse order of derivatives, as dq^n/dt^n, dq^(n-1)/dt^(n-1), ..., q
   currentTime =  startTime
   currentState = initialState
   stateList = []
   while currentTime < endTime:
      stateList.append(deepcopy(currentState)) #otherwise when currentState gets changed the entries in stateList change with it, because python auto copies by reference instead of value.

      deepestDerivatives = deepestDerivUpdater(currentTime, currentState)
      for varDerivListIndex in range(len(currentState)):
         currentState[varDerivListIndex][0] = deepestDerivatives[varDerivListIndex] #get the part of the state corresponding to this variable
         for derivIndex in list(range(1, len(currentState[varDerivListIndex])))[::-1]:
            currentState[varDerivListIndex][derivIndex] += timestep * currentState[varDerivListIndex][derivIndex-1] #make the previous derivative the next derivative * dt

      currentTime += timestep


   return stateList


def newSolve(startTime, endTime, timestep, initialState, deepestDerivUpdater):
    #doesn't use copy
    #initialState looks like this: [vars, dvars/dt, d^2vars/dt^2, ...]
    #where each entry is a vector (represented as a numpy array) of the variables
    currentTime = startTime
    currentState = initialState
    while currentTime < endTime:
        yield currentState
        for i in range(len(currentState)-2, -1, -1):
            currentState[i] += currentState[i+1]*timestep

        currentState[-1] = deepestDerivUpdater(currentTime, currentState)

        currentTime += timestep


def matGrad(mat, dxs): #in 3D #input is a 3D array that corresponds to the value of f(x) for x in R^3 #dxs is a list of how far away adjacent matrix entries are in coordinate space.
    xLen, yLen, zLen = len(mat), len(mat[0]), len(mat[0,0])
    gradMat = np.zeros([xLen, yLen, zLen, 3])
    for x in range(len(mat)):
        for y in range(len(mat[x])):
            for z in range(len(mat[x,y])):
                #assumes that at the boundary, the function's value just outside is the same as at the boundary.
                #uses symettric finite difference

                if x == 0:
                    forward, backward = mat[x+1,y,z], mat[x,y,z]
                elif x == xLen-1:
                    forward, backward = mat[x,y,z], mat[x-1,y,z]
                else:
                    forward, backward = mat[x+1,y,z], mat[x-1,y,z]

                xComponent = (forward - backward)/(2*dxs[0])

                if y == 0:
                    forward, backward = mat[x,y+1,z], mat[x,y,z]
                elif y == yLen-1:
                    forward, backward = mat[x,y,z], mat[x,y-1,z]
                else:
                    forward, backward = mat[x,y+1,z], mat[x,y-1,z]

                yComponent = (forward - backward)/(2*dxs[1])

                if z == 0:
                    forward, backward = mat[x,y,z+1], mat[x,y,z]
                elif z == zLen-1:
                    forward, backward = mat[x,y,z], mat[x,y,z-1]
                else:
                    forward, backward = mat[x,y,z+1], mat[x,y,z-1]

                zComponent = (forward - backward)/(2*dxs[2])

                gradMat[x,y,z] = [xComponent, yComponent, zComponent]

    return gradMat


def matDiv(mat, dxs): #same but for divergence
    xLen, yLen, zLen = len(mat), len(mat[0]), len(mat[0,0])
    divMat = np.zeros([xLen, yLen, zLen])
    for x in range(len(mat)):
        for y in range(len(mat[x])):
            for z in range(len(mat[x,y])):
                if x == 0:
                    forward, backward = mat[x+1,y,z], mat[x,y,z]
                elif x == xLen-1:
                    forward, backward = mat[x,y,z], mat[x-1,y,z]
                else:
                    forward, backward = mat[x+1,y,z], mat[x-1,y,z]

                xComponent = (forward[0] - backward[0])/(2*dxs[0])

                if y == 0:
                    forward, backward = mat[x,y+1,z], mat[x,y,z]
                elif y == yLen-1:
                    forward, backward = mat[x,y,z], mat[x,y-1,z]
                else:
                    forward, backward = mat[x,y+1,z], mat[x,y-1,z]

                yComponent = (forward[1] - backward[1])/(2*dxs[1])

                if z == 0:
                    forward, backward = mat[x,y,z+1], mat[x,y,z]
                elif z == zLen-1:
                    forward, backward = mat[x,y,z], mat[x,y,z-1]
                else:
                    forward, backward = mat[x,y,z+1], mat[x,y,z-1]

                zComponent = (forward[2] - backward[2])/(2*dxs[2])

                divMat[x,y,z] = xComponent + yComponent + zComponent

    return divMat




def slowHeat():
    #example: heat equation #!!!

    dxs = [.5, .5, .5]
    dt = .1
    zMat, yMat, xMat = np.meshgrid(np.arange(-5, 5, dxs[0]), np.arange(-5, 5, dxs[1]), np.arange(-5, 5, dxs[2]), indexing='ij')
    initialF = e**-((xMat**2+yMat**2+zMat**2)**.5)

    stateList = solve(0, 2, dt, [[matDiv(matGrad(initialF, dxs), dxs), initialF]], lambda t,state: matDiv(matGrad(state[0][1], dxs), dxs))



def unnamedDemo():
    #example: first coord is x value, second is y value, second derivatives are cos(t) and sin(t)
    stateList = solve(0, 4*pi, .01, [[0, 0, 0],[0,0,0]], lambda t,currentState: [cos(t), sin(t)])

    varValueList = []
    for state in stateList:
       varValueInThisState = [state[coordIndex][-1] for coordIndex in range(len(state))]
       varValueList.append(varValueInThisState)

    plt.plot(array(varValueList)[:,0], array(varValueList)[:,1])



def grav():
    #example: first coord is x value, second is y value, second derivatives is force from gravity attracting towards origin
    def deepestDerivUpdater(t, currentState):
       x,y = currentState[0][-1], currentState[1][-1]
       distanceSquaredToOrigin = (x**2+y**2)
       unitVectorToOrigin = (1/((x**2+y**2)**.5)) * array([-x,-y])

       force = (1/distanceSquaredToOrigin) * unitVectorToOrigin

       return force

    stateList = solve(0, 15, .01, [[0,0,1], [0,1,0]], deepestDerivUpdater)
    varValueList = []
    for state in stateList:
       varValueInThisState = [state[coordIndex][-1] for coordIndex in range(len(state))]
       varValueList.append(varValueInThisState)

    plt.plot(array(varValueList)[:,0], array(varValueList)[:,1])



def coupledMass():
    #example: that one double spring mechanics problem from that physics textbook by shankar
    def deepestDerivUpdater(t, currentState):
       x0,x1 = currentState[0][-1], currentState[1][-1]

       return [-2*x0 + x1, x0 - 2*x1]


    stateList = solve(0, 15, .01, [[0,0,.5], [0,.25,-.25]], deepestDerivUpdater)
    varValueList = []
    for state in stateList:
       varValueInThisState = [state[coordIndex][-1] for coordIndex in range(len(state))]
       varValueList.append(varValueInThisState)

    plt.plot(array(varValueList)[:,1]+2, range(len(array(varValueList)[:,1]))) #2 is equi offset for 2nd mass
    plt.plot(array(varValueList)[:,0]+1, range(len(array(varValueList)[:,0]))) #1 is equi offset for 1st mass


