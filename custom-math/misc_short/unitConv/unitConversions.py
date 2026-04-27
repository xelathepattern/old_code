# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:15:51 2021

@author: Xela
"""


import igraph

import numpy as np
from numpy import array

import math

from PIL import Image


def textToConversionArray(text): #scroll to bottom for an example of what text should look like
   return array([conversion.split(' ') for conversion in text.split('\n')])


def makeUnitGraph(unitConversions):
   unitsSet = set({})
   for i in unitConversions[:,:2]:
      for j in i:
         unitsSet.add(j)

   units = list(unitsSet)

   unitGraph = igraph.Graph(directed=True)

   numberOfUnits = len(units)
   unitGraph.add_vertices(numberOfUnits)

   unitGraph.vs["label"] = units

   edgesString = unitConversions[:,:2]
   edges = array([ [0 for j in range(len(edgesString[i]))] for i in range(len(edgesString)) ])


   for i in range(len(edgesString)):
      for j in range(len(edgesString[i])):
         edges[i,j] = units.index(edgesString[i,j])


   unitGraph.add_edges(edges)
   unitGraph.degree(mode='out')

   reciprocalEdges = np.flip(edges, axis=1)
   unitGraph.add_edges(reciprocalEdges)

   precision = 4
   edgeLabelsForward = array([float(i) for i in unitConversions[:,2]])
   edgeLabelsBackward = np.round(np.reciprocal(array(edgeLabelsForward)), 4)
   unitGraph.es["label"] = np.append(edgeLabelsForward, edgeLabelsBackward)
   unitGraph.es["curved"] = np.ones(len(unitGraph.es["label"])) #to avoid edges cluttering each other when plotting


   return unitGraph


def plotUnitGraph(unitGraph):
   layout = unitGraph.layout("kk")

   edgeSizeLambda = lambda x: math.log(x+2)
   edgeSizeFunc = np.vectorize(edgeSizeLambda)

   edgeSizes = edgeSizeFunc(array(unitGraph.es["label"]))
   igraph.plot(unitGraph, "unitGraph.png", layout=layout, margin=50, vertex_label_dist=1.5, edge_width=edgeSizes, edge_arrow_size=edgeSizes/2)
   Image.open('unitGraph.png').show()


def calculateUnitConversionFactor(unitGraph, startUnit, endUnit):
   units = unitGraph.vs['label']

   edgePath = unitGraph.get_shortest_paths(units.index(startUnit), units.index(endUnit), output='epath')[0]
   conversionFactorPath = [unitGraph.es['label'][i] for i in edgePath]
   conversionFactor = np.product(array(conversionFactorPath))

   return conversionFactor


text = \
"""foot inch 12
yard foot 3
mile foot 5280
Smoot inch 67
foot hand 3
barleycorn poppyseed 4
inch barleycorn 3
meter barleycorn 118.11
point twip 20
pica point 12
finger inch .875
stick inch 2
Ramsden's_chain rope 5
rope grade 4
rod cubit 11
cubit shaftment 3
grade pace 2
shaftment palm 2
palm inch 3
Gunter's_chain rod 4
shaftment pace .2
line point 6
poppyseed line 1"""


unitGraph = makeUnitGraph(textToConversionArray(text))
plotUnitGraph(unitGraph)