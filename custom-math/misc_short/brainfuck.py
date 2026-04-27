# -*- coding: utf-8 -*-
"""
Created on Wed May 18 21:30:57 2022

@author: Xela
"""


def matchOpenClose(string, openCharacter='[', closeCharacter=']'):
    openIndices = [i for i in range(len(string)) if string[i] == '[']
    forwardMap = {openIndice:findMatchingClose(string, openIndice, openCharacter=openCharacter, closeCharacter=closeCharacter) for openIndice in openIndices}
    inverseMap = {forwardMap[openIndice]:openIndice for openIndice in openIndices}

    return forwardMap, inverseMap

def findMatchingClose(string, openIndice, openCharacter='[', closeCharacter=']'):
    relativeNestingLevel = 0
    for i in range(openIndice, len(string)):
        if string[i] == openCharacter:
            relativeNestingLevel += 1
        elif string[i] == closeCharacter:
            relativeNestingLevel -= 1
            if relativeNestingLevel == 0:
                return i

class BrainfuckExecution:
    def __init__(self, code):
        self.code = ''
        for char in code:
            if char in {'>', '<', '+', '-', '[', ']', ',', '.',}:
                self.code += char

        self.openBracketMap, self.closeBracketMap = matchOpenClose(self.code)

        self.data = {}

        self.dataPointer = 0
        self.instructionPointer = 0

    def executeOneStep(self):
        if self.instructionPointer == len(self.code):
            return

        thisInstruction = self.code[self.instructionPointer]
        if thisInstruction == '>':
            self.dataPointer += 1

        elif thisInstruction == '<':
            self.dataPointer -=1

        elif thisInstruction == '+':
            self.data[self.dataPointer] = self.data.get(self.dataPointer, 0) + 1

        elif thisInstruction == '-':
            self.data[self.dataPointer] = self.data.get(self.dataPointer, 0) - 1

        elif thisInstruction == '[':
            if self.data.get(self.dataPointer, 0) == 0:
                self.instructionPointer = self.openBracketMap[self.instructionPointer]

        elif thisInstruction == ']':
            if self.data.get(self.dataPointer, 0) != 0:
                self.instructionPointer = self.closeBracketMap[self.instructionPointer]

        elif thisInstruction == ',':
            self.data[self.dataPointer] = ord(input("\nIn: ")[0])

        elif thisInstruction == '.':
            print(f"{chr(self.data.get(self.dataPointer, 0))}", end='')

        self.instructionPointer += 1

    def execute(self):
        while self.instructionPointer < len(self.code):
            self.executeOneStep()
