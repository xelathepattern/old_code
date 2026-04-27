# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 19:08:14 2022

@author: Xela
"""


from algebraClasses import Group


def notBurnside(action, symmetryGroup, set_):
    totalFixedPoints = 0
    for groupElement in symmetryGroup:
        for possibleFixedPoint in set_:
            if action(groupElement, possibleFixedPoint) == possibleFixedPoint:
                totalFixedPoints += 1


    result = totalFixedPoints//len(symmetryGroup)
    return result


#example: number of ways to number the endpoints of a rectangle from one to four, considering two rectangles the same if they can be rotated into each other
#each element of the set is represented by a sequence of numbers corresponding to upper-left,upper-right,bottom-right,and bottom-left endpoints respectively
import itertools
set_ = list(itertools.product('1234', '1234', '1234', '1234'))
set_ = set([numberTuple[0]+numberTuple[1]+numberTuple[2]+numberTuple[3] for numberTuple in set_])

symmetryGroup = Group({0,1}, lambda a,b: (a+b)%2)
action = lambda g, a: (a[2]+a[3]+a[0]+a[1]) if g == 1 else a

print(notBurnside(action, symmetryGroup, set_))
