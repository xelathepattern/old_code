# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 18:25:01 2022

@author: Xela 
"""


class Magma(): #the structure-checking functions will only return in finite time if |Magma| is finite
    def __init__(self, set_, operation):
        self.set, self.operation = set_, operation
        return


    def __iter__(self): #make it so that iterating over theGroup is possible, and is equivalent to iterating over theGroup.set, to match the math speak
        return iter(self.set)


    def __len__(self): #so that len(aGroup) == len(aGroup.set) == the cardinality of aGroup
        return len(self.set)


    def __contains__(self, element):
        return element in self.set


    def checkClosure(self):
        for elementA in self:
            for elementB in self:
                if self.operation(elementA, elementB) not in self:
                    return False

        return True


    def checkIsIdentity(self, claimedIdentity):
        for element in self:
            if self.operation(claimedIdentity, element) != self.operation(element, claimedIdentity) or self.operation(claimedIdentity, element) != element:
                return False


        return True


    def checkIdentityExistence(self):
        for possibleIdentity in self:
            if self.checkIsIdentity(possibleIdentity):
                return True


        return False


    def findIdentity(self):
        for possibleIdentity in self:
            if self.checkIsIdentity(possibleIdentity):
                return possibleIdentity


        return None


    def checkHasInverse(self, elementA, identity): #also returns the inverse if it exists
        for elementB in self:
            if self.operation(elementA, elementB) == self.operation(elementB, elementA) == identity:
                return True


        return False


    def findInverse(self, elementA):
        identity = self.findIdentity()
        for elementB in self:
            if self.operation(elementA, elementB) == self.operation(elementB, elementA) == identity:
                return elementB


        return None


    def checkInverseExistence(self):
        identity = self.findIdentity()

        if identity == None:
            return False #i don't think you can define inverses without an identity. regardless, it wouldn't be a group, and that's really all i care about for now


        for element in self:
            if self.checkHasInverse(element, identity) == False:
                return False


        return True


    def checkAssociativity(self):
        for elementA in self:
            for elementB in self:
                for elementC in self:
                    if self.operation(self.operation(elementA, elementB), elementC) != self.operation(elementA, self.operation(elementB, elementC)):
                        return False


        return True


    def checkIsGroup(self):
        if self.checkClosure() and self.checkInverseExistence() and self.checkAssociativity(): #note that checkInverseExistence() already checks identityExistence
            return True


    def checkIsAbelian(self):
        for a in self:
            for b in self:
                if self.operation(a,b) != self.operation(b,a):
                    return False


        return True


class Group(Magma):
    def __init__(self, set_, operation):
        super().__init__(set_, operation)

        assert(self.checkIsGroup()) #this prevents groups from not being groups


    def checkIsNormalSubgroup(self, claimedKernel):
        for g in self:
            for h in claimedKernel:
                if self.operation(self.operation(g, h), self.findInverse(g)) not in claimedKernel:
                    return False


        return True


    def __truediv__(self, kernel): #__truediv__ is how python divides when using a single slash.
        assert(self.checkIsNormalSubgroup(kernel))
