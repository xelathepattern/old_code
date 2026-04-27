# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 12:59:15 2022

@author: Xela
"""


import math
from numpy import inf

from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from functools import reduce #only used for the vertToPoint demo, because it's too sweet not to use

import tkinter as tk
#from icecream import ic

#The drag and drop functionality was heavily inspired by the source code of tkinter.dnd, as I originally tried to use it but switched midway to making my own less confusing (and less general) version.

class Point:
    def __init__(self, *args, color='green', custom_motion_func=lambda mouseGraphPos, **kwargs: mouseGraphPos, custom_constraint_vars={}): #!!!
        self.color = color
        self.custom_motion_func = custom_motion_func
        self.custom_constraint_vars = custom_constraint_vars
        if len(args) == 2: #ex: Point(1,1)
            self.x, self.y = args
        elif len(args) == 1 and len(args[0]) == 2: #ex: Point([1,1]])
            self.x, self.y = args[0]

    def reinit(self):
        self.__init__(self.x, self.y, color=self.color, custom_motion_func=self.custom_motion_func, custom_constraint_vars=self.custom_constraint_vars)

    def plot(self, ax=plt.gca(), color=None):
        if color == None:
            color = self.color
        ax.plot(self.x, self.y, '.', color=color, markersize=10)

    def distance(self, point2):
        return ((point2.y - self.y)**2 + (point2.x - self.x)**2)**.5

    def __hash__(self): #for some reason this method is already on the other classes but not on this one, and it's necessary to put points into sets or dicts
        return hash((self.x, self.y,)) #!!!this may cause errors when checking for inclusion with two overlapping points, since they are treated as the same.

    def __eq__(self, point2): #!!!correct for round errors with a precision var
        PRECISION = .0001
        if type(point2) == Point:
            return (abs(self.x - point2.x) < PRECISION and abs(self.y - point2.y) < PRECISION)
        elif '__len__' in dir(point2) and len(point2) == 2:
            return (abs(self.x - point2[0]) < PRECISION and abs(self.y - point2[1]) < PRECISION)
        elif type(point2) == None:
            return False

    def __add__(self, point2):
        return Point(self.x + point2.x, self.y + point2.y)

    def __rmul__(self, scalar):
        return Point(self.x*scalar, self.y*scalar)

    def __mul__(self, scalarOrPoint):
        if type(scalarOrPoint) == Point:
            return self.x*scalarOrPoint.x + self.y*scalarOrPoint.y
        else:
            return self.__rmul__(scalarOrPoint)

    def __sub__(self, point2):
        return self + -1*point2

    def __truediv__(self, scalar):
        return self*(1/scalar)

    def __repr__(self): # __repr__ gets a canonical string representation of the object, with the expectation that it is valid python code
        return f"Point({self.x}, {self.y})"

    def __str__(self): # __str__ is whats printed, and has no expectation of being valid code
        return f"({self.x}, {self.y})"

    def dnd_start(self, source, event):
       pass

    def dnd_motion(self, source, event):
        mouseImagePos = (source.tkCanvas.canvasx(event.x), source.tkCanvas.canvasy(event.y))
        mouseGraphPos = source.imagePosToGraphPos(mouseImagePos)

        newPos = self.custom_motion_func(mouseGraphPos, **self.custom_constraint_vars)
        #ic(newPos)
        self.x, self.y = newPos.x, newPos.y
        self.reinit()

        source.plot()
        source.canvas.draw()

    def dnd_end(self, source, event):
        source.canvas.draw()


class Line: #!!!breaks for vertical lines
    def __init__(self, point1, slope):
        self.setPoint1 = point1

        self.slope = slope
        self.yIntercept = (point1.y - self.slope * point1.x)

        self.boundingBoxLimits = [[-inf, inf], [-inf, inf]] #this makes Line play nicely with LineSegment -- the inf/-inf here is just a neat way to get a number less/greater than anything else

    def reinit(self):
        self.__init__(self.setPoint1, self.slope)

    def plot(self, ax=plt.gca(), dashed=False, color=None):
        if not dashed:
            if color == None:
                color = 'blue'
            ax.axline((self.setPoint1.x, self.setPoint1.y), slope=self.slope, color=color)
        else:
            if color == None:
                color = 'black'
            ax.axline((self.setPoint1.x, self.setPoint1.y), slope=self.slope, color=color, linestyle='--')

    def findIntersection(self, line2):
        if self.slope == line2.slope:
            return None
        else:
            x = (line2.yIntercept - self.yIntercept)/(self.slope - line2.slope)
            y = self.slope * x + self.yIntercept

            return Point(x, y)

    def pointAlongLine(self, xOffset):
        return Point(self.setPoint1.x + xOffset, self.slope*(self.setPoint1.x + xOffset) + self.yIntercept)

    def closestPointOnLineToPointWithPerpLine(self, toPoint):
        perpindicularLineSlope = -(1/self.slope)

        perpindicularLine = Line(toPoint, perpindicularLineSlope)

        return self.findIntersection(perpindicularLine), perpindicularLine

    def __repr__(self):
        return f"Line({self.setPoint1.__repr__()}, {self.slope})"

    def __str__(self):
        return f"Line({self.setPoint1.__str__()}, {self.slope})"

    def isParallel(self, line2): #!!!test
        return self.slope == line2.slope


X_AXIS = Line(Point(0,0), 0)


class LineSegment(Line):
    def __init__(self, point1, point2,):
        try:
            slope = (point1.y - point2.y)/(point1.x - point2.x)
        except ZeroDivisionError:
            slope = 1000000000


        super().__init__(point1, slope)
        if 'line' not in dir(self):
            self.line = Line(point1, slope)
        else:
            self.line.setPoint1 = point1
            self.line.slope = slope
            self.line.reinit()

        if 'setPoint2' not in dir(self):
            self.setPoint2 = point2
        else:
            self.setPoint2.x, self.setPoint2.y = point2.x, point2.y

        self.length = self.setPoint1.distance(self.setPoint2)
        self.displacement = Point(self.setPoint2.x-self.setPoint1.x, self.setPoint2.y-self.setPoint1.y)

        self.boundingBoxLimits = [[min(self.setPoint1.x, self.setPoint2.x), max(self.setPoint1.x, self.setPoint2.x)], [min(self.setPoint1.y, self.setPoint2.y), max(self.setPoint1.y, self.setPoint2.y)]]

        midpoint = (self.setPoint1 + self.setPoint2)/2
        if 'midpoint' not in dir(self):
            self.midpoint = midpoint
        else:
            self.midpoint.x, self.midpoint.y = midpoint.x, midpoint.y
            self.midpoint.reinit()

    def reinit(self):
        self.__init__(self.setPoint1, self.setPoint2)

    def plot(self, ax=plt.gca(), dashed=False, color=None):
        if not dashed:
            if color == None:
                color = 'C0' #light blue
            ax.plot([self.setPoint1.x, self.setPoint2.x], [self.setPoint1.y, self.setPoint2.y], color=color)
        else:
            if color == None:
                color = 'grey'
            ax.plot([self.setPoint1.x, self.setPoint2.x], [self.setPoint1.y, self.setPoint2.y], color=color, linestyle='--')

        ax.text(self.midpoint.x, self.midpoint.y, f"{round(self.length, 2)}")

    @classmethod #this needs to be a class method so that if given a line, it still works - otherwise lines wouldnt have the ability to check if point is in its bounding box.
    def pointInSegsBounds(cls, segs, point):
        BUFFER = .01 #so that floating point error doesn't cause points to be outside the bounds
        return all([(seg.boundingBoxLimits[0][0] - BUFFER <= point.x <= seg.boundingBoxLimits[0][1] + BUFFER and seg.boundingBoxLimits[1][0] - BUFFER <= point.y <= seg.boundingBoxLimits[1][1] + BUFFER) for seg in segs])

    #!!!TODO: Make segmentize func that takes in a point returning func, some lines/segments, and args for the func, and returns the point if it is in the bounding box of all the segments and returns None otherwise
    def findIntersection(self, line2):
        resultPoint = super().findIntersection(line2)
        if resultPoint == None:
            return None
        elif LineSegment.pointInSegsBounds([self, line2], resultPoint):
            return resultPoint
        else:
            return None

    def pointAlongLine(self, xOffset):
        resultPoint = super().pointAlongLine(xOffset)
        if resultPoint == None:
            return None
        elif LineSegment.pointInSegsBounds([self], resultPoint):
            return resultPoint
        else:
            return None

    def closestPointOnLineToPointWithPerpLine(self, toPoint):
        resultPoint, resultLine = super().closestPointOnLineToPointWithPerpLine(toPoint)
        if resultPoint == None:
            return None
        elif LineSegment.pointInSegsBounds([self], resultPoint):
            return resultPoint, LineSegment(toPoint, resultPoint)
        else:
            return None

    def __repr__(self):
        return f"LineSegment({self.setPoint1.__repr__()}, {self.setPoint2.__repr__()})"

    def __str__(self):
        return f"LineSegment({self.setPoint1.__str__()}, {self.setPoint2.__str__()})"


class Angle: #!!! fix
    DRAW_DIAMETER_PROPORTION = .5
    def __init__(self, startSeg, endSeg, forceSmallerAngle=True): #!!!make special case for perpindicular lines, horiz lines and vert lines
        if 'startSeg' in dir(self):
            self.startSeg.setPoint1.x, self.startSeg.setPoint1.y, self.endSeg.setPoint1.x, self.endSeg.setPoint1.y = startSeg.setPoint1.x, startSeg.setPoint1.y, endSeg.setPoint1.x, endSeg.setPoint1.y
            self.startSeg.setPoint2.x, self.startSeg.setPoint2.y, self.endSeg.setPoint2.x, self.endSeg.setPoint2.y = startSeg.setPoint2.x, startSeg.setPoint2.y, endSeg.setPoint2.x, endSeg.setPoint2.y
            self.startSeg.reinit(), self.endSeg.reinit()
        else:
            self.startSeg, self.endSeg, = startSeg, endSeg,

        self.forceSmallerAngle = forceSmallerAngle
        anchorPoint = startSeg.line.findIntersection(endSeg.line)
        if 'anchorPoint' in dir(self):
            self.anchorPoint.x = anchorPoint.x
            self.anchorPoint.y = anchorPoint.y
            self.anchorPoint.reinit()
        else:
            self.anchorPoint = anchorPoint

        self.startNonAnchor = self.startSeg.setPoint1 if self.startSeg.setPoint1 != self.anchorPoint else self.startSeg.setPoint2 #!!!test
        self.endNonAnchor = self.endSeg.setPoint1 if self.endSeg.setPoint1 != self.anchorPoint else self.endSeg.setPoint2 #!!!test

        self.xAxisToStartAngleLength = math.atan((startSeg.slope - X_AXIS.slope)/(1 + startSeg.slope*X_AXIS.slope))
        if self.startNonAnchor.x < self.anchorPoint.x:
            self.xAxisToStartAngleLength += math.pi

        self.radians = math.acos((self.startSeg.displacement.x * self.endSeg.displacement.x + self.startSeg.displacement.y * self.endSeg.displacement.y) / (self.startSeg.length*self.endSeg.length)) #=\frac{a\cdot b}{\| a \| \| b \|}=\| a \| \| b \| \cos(\theta)

        #the above needs correcting for quadrant reasons, which happens below
        self.baseV1 = self.startNonAnchor - self.anchorPoint
        self.baseV2 = Point(-self.baseV1.y, self.baseV1.x)

        #!!!fix orientation code
        self.coord1, self.coord2 = (self.baseV1*(self.endNonAnchor-self.anchorPoint)), (self.baseV2*(self.endNonAnchor-self.anchorPoint))

        self.xOrientation, self.yOrientation = 1 if self.coord1>0 else -1, 1 if self.coord2>0 else -1
        if self.xOrientation == 1 and self.yOrientation == 1:
            self.radians = math.pi - self.radians
        elif self.xOrientation == -1 and self.yOrientation == 1:
            self.radians = math.pi - self.radians
        elif self.xOrientation == -1 and self.yOrientation == -1:
            self.radians = math.pi - self.radians
            self.radians *= -1
        elif self.xOrientation == 1 and self.yOrientation == -1:
            self.radians += math.pi

        #ic(self.xOrientation, self.yOrientation, self.coord1, self.coord2, self.baseV1, self.baseV2)

        if self.startNonAnchor.x < self.anchorPoint.x:
            pass

        self.radians %= (2*math.pi)
        self.degrees = self.radians * (180/math.pi)

        #ic(self.degrees)
        #ic(self.forceSmallerAngle)
        if self.forceSmallerAngle and self.radians > math.pi:
            #ic(self.startSeg, self.endSeg)
            self.startSeg, self.endSeg = self.endSeg, self.startSeg
            #ic(self.startSeg, self.endSeg)
            self.reinit()
            #ic(self.degrees)


    def reinit(self):
        self.__init__(self.startSeg, self.endSeg, forceSmallerAngle=self.forceSmallerAngle)

    def plot(self, ax=plt.gca()):
        diameter = self.DRAW_DIAMETER_PROPORTION * min(self.startSeg.length, self.endSeg.length)
        arc = patches.Arc((self.anchorPoint.x, self.anchorPoint.y), diameter, diameter, angle=self.xAxisToStartAngleLength*(180/math.pi), theta2=self.degrees)
        ax.text(self.anchorPoint.x, self.anchorPoint.y, f"{round(self.degrees, 1)}°")
        self.arcObj = arc
        ax.add_patch(arc)


class Triangle: #!!!fix angle selection
    def __init__(self, vert1, vert2, vert3):
        self.vertice1, self.vertice2, self.vertice3 = vert1, vert2, vert3

        side1, side2, side3 = LineSegment(self.vertice1, self.vertice2), LineSegment(self.vertice2, self.vertice3), LineSegment(self.vertice3, self.vertice1)
        #if reinitingMode:
        #    print('debug')
        #    self.side1.reinit(), self.side2.reinit(), self.side3.reinit()
        #else:
        self.side1, self.side2, self.side3 = side1, side2, side3

        if 'angle1' not in dir(self):
            self.angle1, self.angle2, self.angle3 = Angle(self.side2, self.side3, forceSmallerAngle=True), Angle(self.side1, self.side3, forceSmallerAngle=True), Angle(self.side2, self.side1, forceSmallerAngle=True) #named by the seg that they face
        else:
            self.angle1.startSeg, self.angle2.startSeg, self.angle3.startSeg = self.side2, self.side1, self.side2
            self.angle1.endSeg, self.angle2.endSeg, self.angle3.endSeg = self.side3, self.side3, self.side1
            self.angle1.reinit(), self.angle2.reinit(), self.angle3.reinit()

        #now for the non-required cool stuff
        centroid = (self.vertice1 + self.vertice2 + self.vertice3)/3
        if 'centroid' not in dir(self):
            self.centroid = centroid
        else:
            self.centroid.x, self.centroid.y = centroid.x, centroid.y

        vertices = [self.vertice1, self.vertice2, self.vertice3]
        checkIfOpposing = lambda seg: lambda vertex: vertex != seg.setPoint1 and vertex != seg.setPoint2 #voila, the magic of currying! checkIfOpposing(seg)(vertex) does the check
        self.opposingVertex1, self.opposingVertex2, self.opposingVertex3 = tuple(filter(checkIfOpposing(self.side1), vertices))[0], tuple(filter(checkIfOpposing(self.side2), vertices))[0], tuple(filter(checkIfOpposing(self.side3), vertices))[0]

        median1, median2, median3 = LineSegment(self.side1.midpoint, self.opposingVertex1), LineSegment(self.side2.midpoint, self.opposingVertex2), LineSegment(self.side3.midpoint, self.opposingVertex3)
        if 'median1' not in dir(self):
            self.median1, self.median2, self.median3 = median1, median2, median3
        else:
            self.median1.setPoint1, self.median2.setPoint1, self.median3.setPoint1 = median1.setPoint1, median2.setPoint1, median3.setPoint1
            self.median1.setPoint2, self.median2.setPoint2, self.median3.setPoint2 = median1.setPoint2, median2.setPoint2, median3.setPoint2
            self.median1.reinit(), self.median2.reinit(), self.median3.reinit()


    def vertToPointSeg(self, point): #!!!make this less kludge
        vertToPointSeg1, vertToPointSeg2, vertToPointSeg3 = LineSegment(self.vertice1, point), LineSegment(self.vertice2, point), LineSegment(self.vertice3, point)
        if 'vertToPointSeg1' not in dir(self):
            self.vertToPointSeg1, self.vertToPointSeg2, self.vertToPointSeg3 = vertToPointSeg1, vertToPointSeg2, vertToPointSeg3
        else:
            self.vertToPointSeg1.setPoint1.x, self.vertToPointSeg2.setPoint1.x, self.vertToPointSeg3.setPoint1.x = vertToPointSeg1.setPoint1.x, vertToPointSeg2.setPoint1.x, vertToPointSeg3.setPoint1.x
            self.vertToPointSeg1.setPoint1.y, self.vertToPointSeg2.setPoint1.y, self.vertToPointSeg3.setPoint1.y = vertToPointSeg1.setPoint1.y, vertToPointSeg2.setPoint1.y, vertToPointSeg3.setPoint1.y

            self.vertToPointSeg1.setPoint2.x, self.vertToPointSeg2.setPoint2.x, self.vertToPointSeg3.setPoint2.x = vertToPointSeg1.setPoint2.x, vertToPointSeg2.setPoint2.x, vertToPointSeg3.setPoint2.x
            self.vertToPointSeg1.setPoint2.y, self.vertToPointSeg2.setPoint2.y, self.vertToPointSeg3.setPoint2.y = vertToPointSeg1.setPoint2.y, vertToPointSeg2.setPoint2.y, vertToPointSeg3.setPoint2.y


    def segToSide(self, point):
        segToSideSeg1, segToSideSeg2, segToSideSeg3 = LineSegment(self.side1.midpoint, point), LineSegment(self.side2.midpoint, point), LineSegment(self.side3.midpoint, point)
        if 'segToSideSeg1' not in dir(self):
            self.segToSideSeg1, self.segToSideSeg2, self.segToSideSeg3 = segToSideSeg1, segToSideSeg2, segToSideSeg3
        else:
            self.segToSideSeg1.setPoint1.x, self.segToSideSeg2.setPoint1.x, self.segToSideSeg3.setPoint1.x = segToSideSeg1.setPoint1.x, segToSideSeg2.setPoint1.x, segToSideSeg3.setPoint1.x
            self.segToSideSeg1.setPoint1.y, self.segToSideSeg2.setPoint1.y, self.segToSideSeg3.setPoint1.y = segToSideSeg1.setPoint1.y, segToSideSeg2.setPoint1.y, segToSideSeg3.setPoint1.y

            self.segToSideSeg1.setPoint2.x, self.segToSideSeg2.setPoint2.x, self.segToSideSeg3.setPoint2.x = segToSideSeg1.setPoint2.x, segToSideSeg2.setPoint2.x, segToSideSeg3.setPoint2.x
            self.segToSideSeg1.setPoint2.y, self.segToSideSeg2.setPoint2.y, self.segToSideSeg3.setPoint2.y = segToSideSeg1.setPoint2.y, segToSideSeg2.setPoint2.y, segToSideSeg3.setPoint2.y

    def reinit(self):
        if 'vertToPointSeg1' not in dir(self): #!!!unkludge and do for seg to side
            if 'segToSideSeg1' not in dir(self):
                self.__init__(self.vertice1, self.vertice2, self.vertice3)
            else:
                segToSides = self.segToSideSeg1, self.segToSideSeg2, self.segToSideSeg3
                self.__init__(self.vertice1, self.vertice2, self.vertice3)
                self.segToSideSeg1, self.segToSideSeg2, self.segToSideSeg3 = segToSides[0], segToSides[1], segToSides[2]
                self.segToSideSeg1.reinit(), self.segToSideSeg2.reinit(), self.segToSideSeg3.reinit()


        else:
            vertToPoints = self.vertToPointSeg1, self.vertToPointSeg2, self.vertToPointSeg3
            if 'segToSideSeg1' not in dir(self):
                self.__init__(self.vertice1, self.vertice2, self.vertice3)
            else:
                segToSides = self.segToSideSeg1, self.segToSideSeg2, self.segToSideSeg3
                self.__init__(self.segToSideSeg1, self.segToSideSeg2, self.segToSideSeg3)
                self.segToSideSeg1, self.segToSideSeg2, self.segToSideSeg3 = segToSides[0], segToSides[1], segToSides[2]
                self.segToSideSeg1.reinit(), self.segToSideSeg2.reinit(), self.segToSideSeg3.reinit()

            self.vertToPointSeg1, self.vertToPointSeg2, self.vertToPointSeg3 = vertToPoints[0], vertToPoints[1], vertToPoints[2]
            self.vertToPointSeg1.reinit(), self.vertToPointSeg2.reinit(), self.vertToPointSeg3.reinit()

    def plot(self, ax=plt.gca()):
        #self.vertice1.plot(ax=ax, color='yellow'), self.vertice2.plot(ax=ax, color='yellow'), self.vertice3.plot(ax=ax, color='yellow'),
        self.side1.plot(ax=ax, color='purple'), self.side2.plot(ax=ax, color='purple'), self.side3.plot(ax=ax, color='purple')


def plotGeoObjects(geoObjects, ax=plt.gca(), clear=False, limits=[[-10, 10], [-10, 10]]):
    if clear == True:
        ax.cla()

    for geoObject in geoObjects:
        geoObject.plot(ax=ax)

    ax.set_xlim(limits[0])
    ax.set_ylim(limits[1])


class GeoCanvas(tk.Canvas):
    def __init__(self, window, geoObjects, ax=plt.gca(), limits=[[-10, 10], [-10, 10]], custom_additional_plotting=lambda self: None, custom_additional_plotting_vars={}):
        self.geoObjects = geoObjects
        self.window = window
        self.fig, self.ax = plt.subplots()
        self.custom_additional_plotting = custom_additional_plotting
        self.custom_additional_plotting_vars = custom_additional_plotting_vars
        self.plot()

        self.points = list(filter(lambda geoObject: type(geoObject).__repr__(geoObject)[:5]=='Point', self.geoObjects)) #using __repr__ to get the class here because for some strange reason (assuming geoObject is a Point), type(geoObject) and type(Point(1,1)) both have the same repr and are otherwise the same but type(geoObject) == type(Point(1,1)) is False

        self.canvas = FigureCanvasTkAgg(self.fig, master=window)
        self.tkCanvas = self.canvas.get_tk_widget()
        self.canvas.draw()

        self.tkCanvas.pack(fill="both", expand=True)
        window.bind('<Configure>', self.resize)
        self.tkCanvas.bind("<ButtonPress-1>", self.dnd_start)

        self.setPosConversion()

    def setPosConversion(self):
        self.axPos = self.ax.get_position()
        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()

        self.window.update() #so that width and height work right
        self.startImagePos = (self.axPos.x0*self.tkCanvas.winfo_width(), self.axPos.y0*self.tkCanvas.winfo_height())
        self.startGraphPos = (self.xlim[0], self.ylim[0])
        self.imageSize = (self.axPos.width * self.tkCanvas.winfo_width(), self.axPos.height * self.tkCanvas.winfo_height())
        self.graphSize = (self.xlim[1]-self.xlim[0], self.ylim[1]-self.ylim[0])

        self.imagePosToGraphPos = lambda imagePos: Point(((imagePos[0] - self.startImagePos[0]) * (self.graphSize[0] / self.imageSize[0])) + self.startGraphPos[0], (((self.tkCanvas.winfo_height()-imagePos[1]) - self.startImagePos[1]) * (self.graphSize[1] / self.imageSize[1])) + self.startGraphPos[1])

    def resize(self, event):
        self.tkCanvas.config(width=event.width, height=event.height)
        self.setPosConversion()

    def plot(self):
        self.ax.cla()
        for obj in self.geoObjects:
            obj.reinit()
        plotGeoObjects(self.geoObjects, ax=self.ax)

        self.custom_additional_plotting(self)

    def dnd_start(self, event):
        #ic("start dnd")
        self.currentDndTargetObject = self.findObjectUnderCursor(event)
        if self.currentDndTargetObject == None: #nothing found under cursor
            return #abort dnd

        self.currentDndTargetObject.dnd_start(self, event)

        self.tkCanvas.bind("<B1-Motion>", lambda event: self.currentDndTargetObject.dnd_motion(self, event))
        self.tkCanvas.bind("<ButtonRelease-1>", self.dnd_end)

    def dnd_end(self, event):
        #ic("end dnd")
        self.currentDndTargetObject.dnd_end(self, event)
        self.tkCanvas.unbind("<B1-Motion>")
        self.tkCanvas.unbind("<ButtonRelease-1>")

    def findObjectUnderCursor(self, event):
        #ic('finding object')
        mouseImagePos = (self.tkCanvas.canvasx(event.x), self.tkCanvas.canvasy(event.y))
        mouseGraphPos = self.imagePosToGraphPos(mouseImagePos)

        DRAGGING_THRESH_RATIO = .02
        draggingThresh = DRAGGING_THRESH_RATIO * min(self.graphSize)
        closestPoint = min(self.points, key=lambda point: point.distance(mouseGraphPos))
        distance = closestPoint.distance(mouseGraphPos)
        foundPoint = closestPoint if distance < draggingThresh else None
        #ic(mouseImagePos, mouseGraphPos, closestPoint, distance, foundPoint)

        return foundPoint


class Circle:
    def __init__(self, center, radiusOrSecondPoint, constrainedPoints=[]):
        self.center = center
        self.constrainedPoints = constrainedPoints

        if type(radiusOrSecondPoint) == float or type(radiusOrSecondPoint) == int:
            self.radius = radiusOrSecondPoint
        else:
            self.radius = radiusOrSecondPoint.distance(self.center)

        def center_motion(mouseAt, circ=self, **kwargs): #!!!this doesn't really work
            for point in circ.constrainedPoints:
                angle = point.custom_constraint_vars['angle'] #preserve angle before and after motion
                print(angle)
                point.x, point.y = circ.center.x+circ.radius*math.cos(angle), circ.center.y+circ.radius*math.sin(angle)
                point.reinit()

            return mouseAt

        self.center.custom_motion_func = center_motion


    def plot(self, ax=plt.gca(), color='red'):
        circPatch = patches.Circle([self.center.x, self.center.y], radius=self.radius, color=color, fill=False)
        ax.add_patch(circPatch)

    def sameAngledPointOnCircle(self, point):
        displacement = point - self.center
        angle = math.atan2(displacement.y, displacement.x)
        newDisplacement = Point(self.radius*math.cos(angle), self.radius*math.sin(angle))
        newPoint = self.center + newDisplacement

        return newPoint

    def constrainPointToCircle(self, point):
        self.constrainedPoints.append(point)
        displacement = point - self.center
        point.custom_constraint_vars['angle'] = math.atan2(displacement.y, displacement.x)

        def constrainedMotion(mouseAt, point=point, circ=self, **kwargs):
            displacement = point - circ.center
            point.custom_constraint_vars['angle'] = math.atan2(displacement.y, displacement.x)

            return self.sameAngledPointOnCircle(mouseAt)

        point.custom_motion_func = constrainedMotion
        point.color = 'fuchsia'
        point.reinit()

    def reinit(self):
        self.__init__(self.center, self.radius, constrainedPoints=self.constrainedPoints)


a,b,c,d = Point(1, 1), Point(-2, -6), Point(3, -5), Point(0, -5)

def demo0():
    seg1, seg2 = LineSegment(a, b), LineSegment(b, c)
    ang = Angle(seg2, seg1)
    geoObjects = [seg1, seg2, a, b, c, ang]

    root = tk.Tk()
    geoCanv = GeoCanvas(root, geoObjects)
    root.mainloop()


def demo1():
    tri = Triangle(a, b, c)
    centroid = tri.centroid

    geoObjects = [a,b,c, tri, centroid, tri.median1, tri.median2, tri.median3, tri.angle1, tri.angle2, tri.angle3]
    root = tk.Tk()
    geoCanv = GeoCanvas(root, geoObjects)
    root.mainloop()


def demo2():
    circ = Circle(a, b.distance(a))
    circ.constrainPointToCircle(b)
    circ.constrainPointToCircle(c)
    circ.constrainPointToCircle(d)

    radSeg1 = LineSegment(a, b)
    radSeg2 = LineSegment(c, a)
    radAngle = Angle(radSeg1, radSeg2)

    inscribedSeg1 = LineSegment(d, b)
    inscribedSeg2 = LineSegment(c, d)
    inscribedAngle = Angle(inscribedSeg1, inscribedSeg2)

    geoObjects = [a,b,c,d, radSeg1,radSeg2,radAngle, circ, inscribedSeg1,inscribedSeg2,inscribedAngle, circ]
    root = tk.Tk()
    geoCanv = GeoCanvas(root, geoObjects)
    root.mainloop()


def demo3(): #!!!not correct
    tri = Triangle(a, b, c)
    tri.vertToPointSeg(d)

    geoObjects = [a,b,c, tri, d, tri.vertToPointSeg1, tri.vertToPointSeg2, tri.vertToPointSeg3]
    def plotBarySum(geoCanv):
        ax = geoCanv.ax
        fig = ax.figure
        vertToPoints = geoCanv.geoObjects[5:]

        vertToPointSum = reduce(lambda acc, vertToPoint: acc+vertToPoint.length, [0, *vertToPoints])

        if 'textObject' not in geoCanv.custom_additional_plotting_vars:
            textObject = fig.text(.5, .9, f"sum = {round(vertToPointSum, 2)}", size='x-large')
            geoCanv.custom_additional_plotting_vars['textObject'] = textObject
        else:
            geoCanv.custom_additional_plotting_vars['textObject'].update({'text': f"sum = {round(vertToPointSum, 2)}"})

    root = tk.Tk()
    geoCanv = GeoCanvas(root, geoObjects, custom_additional_plotting=plotBarySum)
    root.mainloop()


def demo4(): #!!!not correct
    tri = Triangle(a, b, c)
    tri.segToSide(d)

    geoObjects = [a,b,c, tri, d, tri.segToSideSeg1, tri.segToSideSeg2, tri.segToSideSeg3]
    def plotSegToSideSum(geoCanv):
        ax = geoCanv.ax
        fig = ax.figure
        sideToPoints = geoCanv.geoObjects[5:]

        sideToPointSum = reduce(lambda acc, sideToSeg: acc+sideToSeg.length, [0, *sideToPoints])

        if 'textObject' not in geoCanv.custom_additional_plotting_vars:
            textObject = fig.text(.5, .9, f"sum = {round(sideToPointSum, 2)}", size='x-large')
            geoCanv.custom_additional_plotting_vars['textObject'] = textObject
        else:
            geoCanv.custom_additional_plotting_vars['textObject'].update({'text': f"sum = {round(sideToPointSum, 2)}"})

    root = tk.Tk()
    geoCanv = GeoCanvas(root, geoObjects, custom_additional_plotting=plotSegToSideSum)
    root.mainloop()


def demo():
    while True:
        choice = input("(angle|triangle|inscribed|vertToPoint) -> (Angle Demo|Triangle Demo|Inscribed Angle Theorem Demo|Sum Of Vert To Point Demo): ")
        if choice == "angle":
            demo0()
        elif choice == "triangle":
            demo1()
        elif choice == "inscribed":
            demo2()
        elif choice == "vertToPoint":
            demo3()

if __name__ == "__main__":
    demo()
