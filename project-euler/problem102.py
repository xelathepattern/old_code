# -*- coding: utf-8 -*-
"""
Created on Tue May 25 19:18:47 2021

@author: Xela
"""


def dfl(m, c, O): #dfl = distanceFromLine
   o_x, o_y = O

   i_x = (o_y + o_x/m - c)/(m + 1/m)
   i_y = -i_x/m + o_y + o_x/m

   d = ( (o_y - i_y)**2 + (o_x - i_x)**2 )**.5


   return d


def lid(m_1, c_1, m_2, c_2): #lid = lineIntersectDetect


def triangleInteriorDetect(A, B, C, O):
   a_x, a_y, b_x, b_y, c_x, c_y, o_x, o_y = *A, *B, *C, *O



def splitN(text, n):

   #inspired by stackoverflow answer
	return [text[i:i+n] for i in range(0, len(text), n)]


def parseEuler(text):
   triangles = text.replace('\r','').split('\n')
   for i in range(len(triangles)):
      points = splitN(triangles[i].split(','), 2)

      for j in range(len(points)):
         points[j] = (int(points[j][0]), int(points[j][1]))

      triangles[i] = points


   return triangles


def solve(text):
   triangles = parseEuler(text)

   containsOrigin = [triangleInteriorDetect(points[0], points[1], points[2], (0,0)) for points in triangles]


   return sum(containsOrigin)