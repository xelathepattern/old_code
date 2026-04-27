# -*- coding: utf-8 -*-
"""
Created on Mon Mar 8 13:03:47 2021

@author: Xela
"""


import pyautogui

import mouse

from math import sin, cos, tan, pi

from time import sleep

from numpy import arange

from itertools import product

from PIL import Image

import numpy as np

from moviepy.editor import VideoFileClip

import sys

from tqdm import tqdm


def mouseTrace(f, start):
   pyautogui.moveTo(start, f(start), _pause=False)
   pyautogui.mouseDown()

   while (pyautogui.position()[0] < 2230) and (pyautogui.position()[1] < 1450):
      x = pyautogui.position()[0] + 10

      pyautogui.mouseDown(x, f(x))

   pyautogui.mouseUp()



def implicitPoints(f, bounds):
   valSpace = product(arange(*bounds[0]), arange(*bounds[1]))

   points = []
   for point in valSpace:
      if f(*point) == True:
         points.append(point)

   return points


def drawPoints(points):
   for point in points:
      pos = pyautogui.position()
      if (point[0] >= 2230) or (point[1] >= 1440):
         break #this point is out of bounds, go to next point
      elif (pos[1] <= 60) or (pos[1] >= 1450):
         sys.exit() #fail"safe"
      else:
         sleep(.0040000000000000007) #otherwise the points blend together into lines/the points don't show up whilst drawing, only after completion. This was an attempt to get the smallest number that still worked (it can probably be smaller with more effort).
         mouse.move(*point)
         mouse.click()

   return


def drawImplicit(f, bounds):
   drawPoints(implicitPoints(f, bounds))

   return



def digitizeImage(img, rgba=False):
   img = np.array(img, dtype='int64')

   if rgba:
      img = np.delete(img, 3, 2) #to delete the 4th channel on the colors

   red, blue, green = img[:, :, 0], img[:, :, 1], img[:, :, 2]

   #every pixel color is a point in colorspace. find the taxicab distance (using euclidean distance won't change the results since if the euclidean distance is greater then so is the taxicab distance), then see whether it is closest to 0,0,0 or 255,255,255
   distanceFromBlack = red + blue + green
   distanceFromWhite = 255 + 255 + 255 - distanceFromBlack

   digitized = np.greater(distanceFromBlack, distanceFromWhite)

   return digitized


def pointsFromDigitized(digitized):
   points = []
   for point in product(range(len(digitized[0])), range(len(digitized))):
      if digitized[point[1], point[0]] == False: #false is a black pixel
         points.append(point)

   return np.array(points)


def cleanPoints(points, start, stepX, stepY):
   shiftedPoints = points + start

   shiftedPointsStepY = shiftedPoints[::stepY]

   shiftedPointsStepYSortX = sorted(shiftedPointsStepY, key = lambda k: [k[1], k[0]]) #the sorted sorts based on the output of the function passed to the key argument in ascending order. When sorting lists, python sorts it by the first element. This swaps the elements so that it sorts based on the second element, which sorts on the y values, which is what we want

   shiftedPointsStepXYSortX = shiftedPointsStepYSortX[::stepX]


   return shiftedPointsStepXYSortX


def drawImage(img, start, stepX, stepY):
   points = pointsFromDigitized(digitizeImage(img))

   cleanedPoints = cleanPoints(points, start, stepX, stepY)

   drawPoints(cleanedPoints)


   return



def clearScreen():
   pyautogui.hotkey('ctrl', 'a')
   pyautogui.press(['del'])

   return


def drawVideo(videoPath, start, stepX, stepY, stepT):
   clip = VideoFileClip(videoPath)

   frames = tuple(clip.iter_frames())[::stepT]

   for frame in tqdm(frames):
      drawImage(Image.fromarray(frame), start, stepX, stepY)
      clearScreen()
      #reselect draw button
      mouse.move(130, 20)
      mouse.click()
      #move out of the failsafe range
      mouse.move(300, 100)



def digiVideo(videoPath):
   clip = VideoFileClip(videoPath)
   frames = clip.iter_frames()
   digiFrames = []
   for i in frames:
      digiFrames.append(Image.fromarray(digitizeImage(i)))

   return digiFrames



def parabola(x):
   return (((x-1127)**2) // 650) + 200


def mySin(x):
   return 400*(sin(x/100) + 1.875)


def circle(x, y):
   return round((x - 1127)**2 + (y - 750)**2) == 90000



def main():
   #mouseTrace stuff
   #sleep(5)

   #parabola(x):
   #start = 226

   #mySin(x):
   #start = 10

   #mouseTrace(mySin, start)


   #implicitDraw stuff
   #bounds = [ [800, 1500, .5], [400, 1100, .5] ]
   #drawImplicit(circle, bounds)

   #image stuff
   #drawImage(Image.open('rick.png'), (30, 200), 10, 10)

   rickroll_filepath = ""
   drawVideo(rickroll_filepath, pyautogui.position(), 7, 7, 3)


   print("done")


   return


sleep(3)
main()
