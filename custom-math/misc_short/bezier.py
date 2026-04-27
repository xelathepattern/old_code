# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 19:12:48 2022

@author: Xela 
"""


def bezier_0(p1):
    return lambda t: p1


def bezier_next(bezierPrev, pNew):
    return lambda t: bezierPrev(t)*(1-t) + pNew*t


def bezier_n(points):
    runningBezier = bezier_0(points[0])

    for point in points:
        runningBezier = bezier_next(runningBezier, point)

    return runningBezier


def spline(b1, b2):
    return lambda t: b1(2*t) if t <= .5 else b2(2*t)


def nBlock(list_, n):
    blocks = [list_[i:i + n] for i in range(0, len(list_), n)]
    return blocks


def nBezierSpline(points, n):
    pointsForEachCurve = nBlock(points,n)
    bezierCurves = list(map(bezier_n, pointsForEachCurve))

    def outBezier(t):
        tSpacePerCurve = 1/len(bezierCurves)
        curveIndex = int(t//tSpacePerCurve) if t != 1 else -1
        return bezierCurves[curveIndex](t*len(bezierCurves))

    return outBezier
