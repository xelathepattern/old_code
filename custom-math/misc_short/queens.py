# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:15:27 2021

@author: Xela
"""


def queenCanAttack(queenPos, attackPoint):
   #queen's attack is actually just seeing if the slope is 0, undefined, 1, or -1
   yDiff = (attackPoint[1] - queenPos[1])
   xDiff = (attackPoint[0] - queenPos[0])

   if xDiff==0 or yDiff==0 or xDiff==yDiff or xDiff==-yDiff:
      return True
   else:
      return False


def getValidQueenPos(boardDims, forbiddenPoses, queenPoses): #forbidden poses are already tried values
   #print("Harold")
   #print(boardDims)
   #print(forbiddenPoses)
   #print(queenPoses)
   #print("Delorah")
   possibleY = list(range(boardDims[1]))
   possibleX = list(range(boardDims[0]))

   [possibleY.remove(queenPose[1]) for queenPose in queenPoses]
   [possibleX.remove(queenPose[0]) for queenPose in queenPoses]

   for y in possibleY:
      for x in possibleX: #[x,y] is prospective position
         if [x,y] in (forbiddenPoses + queenPoses): #reject if position is forbidden or if a queen is already there
            pass
         else:
            attackable = False
            for [queenX, queenY] in queenPoses:
               if queenCanAttack([queenX, queenY], [x,y]):
                  attackable=True
                  break

            if not attackable:
               return [x,y]



   return None


def solve(boardDims, totalNumberOfQueens):
   currentQueenPoses = []
   forbiddenPosesForEachQueen = [ [  ], ]
   while len(currentQueenPoses) < totalNumberOfQueens:
      #print('in while')
      #print(currentQueenPoses)
      #print(forbiddenPosesForEachQueen)
      placedQueenPos = getValidQueenPos(boardDims, forbiddenPosesForEachQueen[-1], currentQueenPoses)
      #print(placedQueenPos)
      #print('boop')
      if placedQueenPos==None:
         forbiddenPosesForEachQueen.pop()
         forbiddenPosesForEachQueen[-1].append(currentQueenPoses.pop())
      else:
         currentQueenPoses.append(placedQueenPos)
         forbiddenPosesForEachQueen.append([])


   return currentQueenPoses


#!!! make a chessboard visualizer



solveN = lambda n: solve((n,n), n)

n=8
print(solveN(n))