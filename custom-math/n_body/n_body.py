# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 22:04:00 2021

@author: Xela
"""



from math import atan2 as arctan2
from math import sin, cos, pi

from numpy import array

from plot3d import plot3dPoints

import matplotlib
import matplotlib.pyplot as plt


from tqdm import tqdm

from imageio import imread, mimsave

from datetime import datetime

import os


class body:
   def __init__(self, mass, pos, velocity): #velocity is a vector in cartesian coords
      self.mass, self.pos, self.velocity = mass, pos, velocity

      #circle is a function describing the circle that is the body.
      density = 1
      volume = mass/density
      #radius = (3/(4*pi) * volume) ** 1/3 [this is volume of sphere but solving for r]
      precision = 2
      self.radius = round( ((3/(4*pi))*volume)**(1/3), precision)


def cartToPolar(vector):
   x = vector[0]
   y = vector[1]

   #due to some trig, theta = arctan(relY/relX) + (quadrant - 1) * pi/2 [when zero indexed it's just quadrant * pi/2]
   #however, arctan2 takes into account the quadrants for us, so just arctan(relY/relX)

   theta = arctan2(y, x)

   #via pythagorean theorem, r = sqrt(x^2+y^2)
   r = (x**2 + y**2)**.5

   return r, theta


def polarToCart(r, theta):
   return r*cos(theta), r*sin(theta)


def findAcceleration(body0, body1): #body0 is this body, body1 is the body being attracted to
   gravitationalConstant = 1e2 #real life is ~ 6.6743e-11

   #find the direction to body1 from body0
   #transform it so body0 is at 0,0 and then find the direction to body1
   relX = body1.pos[0] - body0.pos[0]
   relY = body1.pos[1] - body0.pos[1]

   _, theta = cartToPolar((relX, relY)) #the direction towards the body

   #acceleration = gravitationalConstant * mass/d**2 [where d is the distance, mass is the mass of the body this is being attracted to]
   distance = (relX**2 + relY**2)**.5

   magnitude = gravitationalConstant * body1.mass/distance**2

   return polarToCart(magnitude, theta)


def findDeltaV(acceleration, dt):
   return (acceleration[0]*dt, acceleration[1]*dt)


def findDeltaPos(velocity, dt):
   return (velocity[0]*dt, velocity[1]*dt)


def cartAdd(vector0, vector1):
   return (vector0[0] + vector1[0]), (vector0[1] + vector1[1])


def sim(bodies, dt, timeEnd, dynamicDt=False):
   time = 0
   bodiesTimeList = [ (0, [body(j.mass, array(j.pos), array(j.velocity)) for j in bodies]) ] #contains a list of tuples, where each tuple is (time, bodiesAtThisTime)

   tqdm.write("Simulating bodies...")
   pbar = tqdm(total=timeEnd)
   dtOriginal = dt
   while time < timeEnd:
      #stuff that changes dt according to distances
      #NOTE: the dynamic dt changing doesn't work well.
      #TODO: Make it work well.
      if dynamicDt == True:
         bodiesAtThisTime = [] #this variable is the bodies at the time the iteration is working on
         unorganizedDistances = []
         bodies = bodiesTimeList[-1][1] #this makes sure we use the bodies from the previous time and not the ones updated for this time.
         for i in range(len(bodies)):

            thisBody = body(bodies[i].mass, bodies[i].pos, bodies[i].velocity) #creating a new instance of the class so fiddling with it doesn't fiddle with the original
            otherBodies = bodies[:i] + bodies[i+1:] #this just gets a list of every body but this one

            for otherBody in otherBodies:
               safeOtherBody = body(otherBody.mass, otherBody.pos, otherBody.velocity)
               relX = thisBody.pos[0] - safeOtherBody.pos[0]
               relY = thisBody.pos[1] - safeOtherBody.pos[1]

               distance = (relX**2 + relY**2)**.5 - thisBody.radius - safeOtherBody.radius #this way we get the distance between the radii of the bodies.

               unorganizedDistances.append(distance)

         try:
            smallestDistance = min(unorganizedDistances)

            dtMod = .5 * (smallestDistance**2)

            dtModMin = .01
            dtModMax = 1.5

            if dtMod < dtModMin:
               dtMod = dtModMin
            elif dtMod > dtModMax:
               dtMod = dtModMax

         except ValueError: #happens when no other bodies to get a distance from, and min([]) is a ValueError
            dtMod = 1

         dt = dtOriginal * dtMod



      bodiesAtThisTime = [] #this variable is the bodies at the time the iteration is working on
      collidedIndices = set()
      bodies = bodiesTimeList[-1][1] #this makes sure we use the bodies from the previous time and not the ones updated for this time.
      for i in range(len(bodies)):
         if (i not in collidedIndices):
            thisBody = body(bodies[i].mass, bodies[i].pos, bodies[i].velocity) #creating a new instance of the class so fiddling with it doesn't fiddle with the original
            otherBodies = bodies[:i] + bodies[i+1:] #this just gets a list of every body but this one

            deltaPos = array(findDeltaPos(thisBody.velocity, dt))
            thisBody.pos = thisBody.pos + deltaPos

            totalAcceleration = array((0,0))


            for j in range(len(otherBodies)):
               #transform the j indice into what the i indice would be
               if j >= i:
                  iOfJ = j + 1
               if j < i:
                  iOfJ = j

               if (iOfJ) not in collidedIndices:
                  otherBody = otherBodies[j]
                  safeOtherBody = body(otherBody.mass, otherBody.pos, otherBody.velocity)

                  relX = safeOtherBody.pos[0] - thisBody.pos[0]
                  relY = safeOtherBody.pos[1] - thisBody.pos[1]

                  distance = (relX**2 + relY**2)**.5

                  collisionDistance = thisBody.radius + safeOtherBody.radius #max distance between two tangent circles is sum of their radii
                  safetyBuffer = .1 #this stops bodies from getting close enough that things start going wonk
                  collisionDistance += safetyBuffer
                  if distance < collisionDistance:
                     m_1 = thisBody.mass
                     m_2 = safeOtherBody.mass

                     #v_3 = (m_1 + m_2 + v_1 + v_2) / (m_1 + m_2) thanks to conservation of momentum

                     tmp1 = cartAdd(thisBody.velocity, safeOtherBody.velocity)
                     tmp2 = cartToPolar(tmp1)

                     newMass = m_1 + m_2

                     newVelocity = polarToCart( ((newMass + tmp2[0]) / newMass), tmp2[1])



                     thisBody.mass = newMass
                     thisBody.velocity = newVelocity

                     #new position is going to be where the two bodies's circles touch
                     #this is same as going r units in the direction of the other body's center
                     #take the direction to the body's center, then make a vector with magnitude of thisBody.radius and with that direction
                     #find direction to the body's center by finding the relX and relY difference between the two points with otherBody.x-thisBody.x,otherBody.y-thisBody.y
                     #take the direcction of that vector, set the magnitude to thisBody.radius, then add it to thisBody.position
                     #already have relX and relY from outside the for loop
                     _, direction = cartToPolar((relX, relY))
                     addendVector = polarToCart(thisBody.radius, direction)

                     thisBody.pos = cartAdd(thisBody.pos, addendVector)


                     #print("collision! %s" % iOfJ)

                     collidedIndices.add(iOfJ)


                  acceleration = array(findAcceleration(thisBody, safeOtherBody))

                  totalAcceleration = totalAcceleration + acceleration


            deltaV = array(findDeltaV(totalAcceleration, dt))
            thisBody.velocity = thisBody.velocity + deltaV

            bodiesAtThisTime.append(body(thisBody.mass, thisBody.pos, thisBody.velocity))


      if time != 0:
         pbar.update(dt)

      time += dt
      bodiesTimeList.append( (time, bodiesAtThisTime) )



   return bodiesTimeList


def makePosTimeList(bodiesTimeList):
   posTimeList = []
   for i in bodiesTimeList:
      time = i[0]
      bodiesAtThisTime = i[1]

      posAtThisTime = array([j.pos for j in bodiesAtThisTime])
      radiiAtThisTime = array([j.radius for j in bodiesAtThisTime])

      posTimeList.append( (time, posAtThisTime, radiiAtThisTime) )

   return posTimeList


def visi3d(posTimeList):
   points = []
   for i in posTimeList:
      for pos in i[1]:
         points.append( (pos[0], pos[1], i[0]) )

   plt.figure('visi3d')

   fig, ax = plot3dPoints(points, labels=['x','y','t'])

   #TODO: plot the circles too
   #idea: google matplotlib flat shape on 3d plot, iterate through each time slice and each body in said time slice to draw the circle.

   return fig, ax


def makeAnimation(posTimeList, window):
   posListOverTime = array([timeAndPos[1] for timeAndPos in posTimeList], dtype='object') #basically turn a list of form [(time_1, posAtTime_1), (time_2, posAtTime_2), ...] into a list of form [posAtTime_1, posAtTime_2, ...]
   radiiListOverTime = array([timeAndPos[2] for timeAndPos in posTimeList], dtype='object') #the dtype='object' stuff is to stop matplotlib from saying that it is deprecated. idk why this is really necessary, something something ragged nested sequences

   tqdm.write("Plotting frames...")
   matplotlib.use('Agg')
   for i in tqdm(range(len(posListOverTime))):
      posAtThisTime = posListOverTime[i]
      radiiAtThisTime = radiiListOverTime[i]

      x, y = posAtThisTime[:,0], posAtThisTime[:,1]


      fig = plt.figure("posAtThisTime%s" % i)
      ax = fig.gca()

      #plot the points
      scalingNumber = 250
      ax.scatter(x, y, s=[scalingNumber * radius**2 for radius in radiiAtThisTime]) #scalingNumber scales the size to be in units of 1 unit instead of points. Found via guesstimation/guesstimath and manually fiddling with it till it looked right.



      timePrecision = 10
      plt.title("Time: %s" % ( round(posTimeList[i][0], timePrecision) ) )

      plt.xlim(*window[0])
      plt.ylim(*window[1])


      plt.savefig('plots/frames/frame%s.png' % i)
      plt.close()



   images = []
   for frame in range(len(posListOverTime)):
      images.append(imread('plots/frames/frame%s.png' % frame))


   timestamp = str(datetime.now()).replace(':', '-').replace('.', '-')

   mimsave('plots/n_body%s.mp4' % timestamp, images, quality=7)


   return timestamp


dt = .01
timeEnd = 5
dynamicDt = True
posTimeList = makePosTimeList(sim([body(4, (2,-5), (-2,-3)), body(1, (5,5), (-2,5)), body(4, (-3,4), (1,-2)), body(5, (-20, -15), (-1,-1))], dt, timeEnd, dynamicDt=dynamicDt))

matplotlib.use('Agg')

timestamp = makeAnimation(posTimeList, [ [-30, 10], [-30, 10] ])

os.startfile(os.getcwd()+'\\plots\\n_body%s.mp4' %  timestamp)

fig, ax = visi3d(posTimeList)
