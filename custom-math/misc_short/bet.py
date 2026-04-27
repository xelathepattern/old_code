# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 08:38:09 2022

@author: Xela 
"""


import sys


def calculateEV(odd1, odd2, prob1):
    return odd1*prob1 - odd2*(1-prob1)


def calculateOtherOdd(odd1, prob1, prob2):
    #odd1:odd2, person betting on odd1 believes odd1 with prob1 certainty, and person betting on odd2 believes odd1 with prob2 certainty
    return (odd1*prob1 + odd1*prob2)/(2 - prob1 - prob2)


def calculateOddsProportion(prob1, prob2):
    #returns odd1/odd2
    return (1-prob1+prob2)/(1-prob2+prob1)


def main():
    firstIter = True
    lastIter = False
    while not lastIter:
        if len(sys.argv) > 3 and firstIter:
            if len(sys.argv) > 4:
                if bool(sys.argv[4]):
                    lastIter = True

            prob1, prob2, odd1 = sys.argv[1:4]
        else:
            args = input("Input prob1 prob2 odd1 optionalStop: ").split(' ')
            if len(args) == 4:
                if bool(args[3]):
                    lastIter = True

            prob1, prob2, odd1 = args[0:3]

        prob1, prob2, odd1 = float(prob1), float(prob2), float(odd1)

        if len(sys.argv) > 5:
            if sys.argv[5]:
                fname = sys.argv[5]
            else:
                fname = None
        else:
            fname = None

        odd2 = calculateOtherOdd(odd1, prob1, prob2)
        ev = calculateEV(odd1, odd2, prob1)

        reverseBet = False
        if ev < 0:
            reverseBet = True
            prob1, prob2 = prob2, prob1
            ev = -ev

        if fname:
            with open(fname, 'w') as f:
                if reverseBet:
                    f.write("person2 : person1\n")
                else:
                    f.write("person1 : person2\n")
                f.write(f"{odd1} : {odd2}, ev={ev}")
        else:
            if reverseBet:
                print("person2 : person1")
            print(f"{odd1} : {odd2}, ev={ev}")

        firstIter = False


main()
