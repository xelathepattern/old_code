# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 12:02:01 2022

@author: xela
"""


import math
import collections

import copy

from tqdm import tqdm

import random

WORD_FILE = 'dictionary.txt'
WORDLE_LEN = 5

with open(WORD_FILE) as f:
    WORD_SET = set(f.read().split('\n'))

WORDS_TO_REMOVE = set({})
for word in WORD_SET:
    if len(word) != WORDLE_LEN:
        WORDS_TO_REMOVE.add(word) #can't just remove from the WORD_SET directly because set can't change size during a loop iterating over it's elements

WORD_SET.symmetric_difference_update(WORDS_TO_REMOVE)
WORD_TUPLE = tuple(WORD_SET)

EMPTY_HINT = {'knownLetterPoses':{}, 'knownLetterNotInPoses': {}, 'knownAtLeastLetterCounts':{}, 'knownExactLetterCounts':{}, 'knownPresents':set([]), 'forbiddens':set([])}
FIRST_GUESS = 'tares'


def checkWord(hintState, word):
    for forbidden in hintState['forbiddens']:
        if forbidden in word:
            return False

    if not hintState['knownPresents'].issubset(word):
        return False

    knownLetterNotInPoses = hintState['knownLetterNotInPoses']
    for knownNotInPos in knownLetterNotInPoses.keys():
        if word[knownNotInPos] in knownLetterNotInPoses[knownNotInPos]:
            return False

    knownLetterPoses = hintState['knownLetterPoses']
    for knownPos in knownLetterPoses.keys():
        if word[knownPos] != knownLetterPoses[knownPos]:
            return False


    counts = collections.Counter(word)
    for knownLetterCountLetter in hintState['knownExactLetterCounts'].keys():
        if hintState['knownExactLetterCounts'][knownLetterCountLetter] != counts[knownLetterCountLetter]:
            return False

    for knownLetterCountLetter in hintState['knownAtLeastLetterCounts'].keys():
        if hintState['knownAtLeastLetterCounts'][knownLetterCountLetter] > counts[knownLetterCountLetter]:
            return False

    return True


def findValidWords(hintState, prevPossWords=WORD_SET):
    words = set({})
    for word in prevPossWords:
        if checkWord(hintState, word):
            words.add(word)

    return words


def countValidWords(hintState, prevPossWords=WORD_SET):
    count = 0
    for word in prevPossWords:
        if checkWord(hintState, word):
            count += 1

    return count


def negentropyOfWordState(numOfWordStates): #negentropy is -entropy. i know, so clever. we're using negentropy so that higher ev = larger negentropy = smaller entropy
    return -math.log(numOfWordStates, 2)


def newHintState(prevHintState, realWord, guess):
    newHintState = copy.deepcopy(prevHintState)
    specialCaseRealCounts = collections.Counter(realWord)
    specialCaseGuessCounts = collections.Counter(guess)

    _ = tuple(map(lambda word: specialCaseRealCounts.pop(word), [word for word in specialCaseRealCounts if specialCaseRealCounts[word]<1]))
    _ = tuple(map(lambda word: specialCaseGuessCounts.pop(word), [word for word in specialCaseGuessCounts if specialCaseGuessCounts[word]<1]))

    for i in range(len(guess)):
        if guess[i] == realWord[i]:
            newHintState['knownLetterPoses'][i] = guess[i]
        elif guess[i] in realWord:
            newHintState['knownPresents'].add(guess[i])

            if guess[i] in specialCaseGuessCounts:
                if specialCaseGuessCounts[guess[i]] > specialCaseRealCounts[guess[i]]:
                    newHintState['knownExactLetterCounts'][guess[i]] = specialCaseRealCounts[guess[i]]
                else:
                    newHintState['knownAtLeastLetterCounts'][guess[i]] = specialCaseGuessCounts[guess[i]]

            if i in newHintState['knownLetterNotInPoses']:
                newHintState['knownLetterNotInPoses'][i].add(guess[i])
            else:
                newHintState['knownLetterNotInPoses'][i] = set([guess[i]])


        else:
            newHintState['forbiddens'].add(guess[i])

    return NestableDict(newHintState)


class NestableDict: #circumvent the fact that for some reason dictionaries aren't hashable but objects with dictionaries are
    def __init__(self, normalDict):
        self.normalDict = {}
        for key in normalDict.keys():
            self.normalDict[key] = normalDict[key]


def findPossibleHintStatesWithCauseWords(prevHintState, guess):
    hintStateDict = {}
    for possibleRealWord in findValidWords(prevHintState):
        effectHint = newHintState(prevHintState, possibleRealWord, guess)
        if effectHint in hintStateDict.keys():
            hintStateDict[effectHint].add(possibleRealWord)
        else:
            hintStateDict[effectHint] = set({possibleRealWord})

    return hintStateDict


def ev(prevHintState, guess, wordsToCheck=WORD_SET): #!!!account for fact that sometimes guessing with non-guaranteed correctedness is better than choosing most informative word

    prevPossWords = wordsToCheck

    #if not checkWord(prevHintState, guess):
        #return 0

    startEntropy = negentropyOfWordState(len(prevPossWords))

    possHintsWithCauses = findPossibleHintStatesWithCauseWords(prevHintState, guess)
    runningEV = 0
    for hintState in possHintsWithCauses.keys():
        probOfState = len(possHintsWithCauses[hintState])/len(prevPossWords)
        valueOfState = negentropyOfWordState(countValidWords(hintState.normalDict, prevPossWords=prevPossWords)) - startEntropy

        runningEV += probOfState*valueOfState

    return runningEV


def decide(prevHintState, searchOnlyPossThresh=150): #searchOnlyPossThresh is the thresh where if len(prevPossWords) is big enough we just search prevPossWords instead of all words
    prevPossWords = findValidWords(prevHintState)
    prevPossWordsSize = len(prevPossWords)
    print(f"There are {prevPossWordsSize} possible words")
    if prevPossWordsSize == 1:
        print([list(prevPossWords)[0], 0])
        return [list(prevPossWords)[0], 0]

    bestEvWord = ['DEFWOR', 0] #DEFWOR is just a dummy placeholder word.

    #the only possible real words are different than the possible guesses - optimal guesses are not necessarily those that are probably correct, but rather those that give the most information
    if prevPossWordsSize > searchOnlyPossThresh:
        guessSearchSpace = prevPossWords
    else:
        guessSearchSpace = WORD_SET

    for possWord in tqdm(guessSearchSpace):
        thisEv = ev(prevHintState, possWord, wordsToCheck=prevPossWords)
        if thisEv > bestEvWord[1]:
            bestEvWord = [possWord, thisEv]
            print(bestEvWord)

    return bestEvWord


def playWordle(realWord=None):
    if realWord==None:
        realWord = random.choice(WORD_TUPLE)

    print(f"real: {realWord}")
    hintState = EMPTY_HINT
    guess = FIRST_GUESS #start with precomputed/pulled out of hat guess to avoid super lengthy initial computation.
    numGuesses = 1
    while guess != realWord:
        hintState = newHintState(hintState, realWord, guess).normalDict
        print(hintState)
        guess = decide(hintState)[0]
        print(guess)
        numGuesses += 1

    return realWord, numGuesses


def wordleStats(numRuns, tryAll=False):
    realWordStats = {}

    if not tryAll:
        for _ in range(numRuns):
            playResult = playWordle()
            realWordStats[playResult[0]] = playResult[1]
    else:
        for word in WORD_SET:
            playResult = playWordle(realWord=word)
            realWordStats[playResult[0]] = playResult[1]

    return realWordStats


def updateHint(prevHintState, updateStr, inplace=False): #!!!fix multiple letter problem
    letters = updateStr[::2]
    colors = updateStr[1::2]
    if not inplace:
        newHintState = copy.deepcopy(prevHintState)
    else:
        newHintState = prevHintState

    for i in range(len(letters)):
        if colors[i] == 'g':
            newHintState['knownLetterPoses'][i] = letters[i]
        elif colors[i] == 'y':
            newHintState['knownPresents'].add(letters[i])

            if i in newHintState['knownLetterNotInPoses'].keys():
                newHintState['knownLetterNotInPoses'][i].add(letters[i])
            else:
                newHintState['knownLetterNotInPoses'][i] = set([letters[i]])
        elif colors[i] == 'f': #for forbidden
            newHintState['forbiddens'].add(letters[i])

    return newHintState


def externalWordle():
    while True:
        prevHintState = EMPTY_HINT
        guess = FIRST_GUESS
        while True:
            updateStr = input(f"{guess}: ")
            if updateStr[1::2] == 'g'*len(updateStr[1::2]):
                break
            prevHintState = updateHint(prevHintState, updateStr)

            guess = decide(prevHintState)[0] #!!!efficiency note - doesn't keep possible words between decisions...
            possWords = findValidWords(prevHintState)
            viewPossWords = input(f'There are {len(possWords)}. View possWords (y/n)? ')
            if viewPossWords == 'y':
                print(possWords)


#hintState = updateHint(EMPTY_HINT, 'cfrfafnfey')
#decide(hintState)
externalWordle()
