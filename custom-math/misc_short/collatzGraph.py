# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 20:23:32 2021

@author: Xela
"""


import networkx as nx
import matplotlib.pyplot as plt

from tqdm import tqdm


def collatz(n, oldGraph=None, plotGraph=True):
   steps = 0

   if oldGraph:
      graph = oldGraph
   else:
      graph = nx.DiGraph()

   while n != 1:
      if not(n%2):
         graph.add_edge(n, n//2)

         n = n//2
      else:
         graph.add_edge(n, 3*n + 1)

         n = 3*n + 1


   if plotGraph:
      nx.draw(graph, with_labels=True)


   return graph


def collatzGraph(n, plotGraph=True):
   oldGraph = None
   for i in tqdm(range(1, n)):
      oldGraph = collatz(i, oldGraph=oldGraph, plotGraph=False)


   if plotGraph:
      nx.draw(oldGraph, with_labels=True)


   return oldGraph

graph = collatzGraph(50)