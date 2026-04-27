# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 15:14:47 2022

@author: Xela 
"""


import math
import collections


def rollingSubsequences(sequence, subLen):
    getSubAtPos = lambda pos: sequence[pos:pos+subLen]

    return tuple(map(getSubAtPos, range(len(sequence) - subLen + 1)))


def scoreHypoth(realSeq, seqHypoth, hypothLen, options=None):
    if options == None:
        options = set(realSeq)

    subSeqs = rollingSubsequences(realSeq, hypothLen+1)

    running = 0
    for seq in subSeqs:
        running += math.log(seqHypoth[seq[:-1]][seq[-1]], 2)

    return running - hypothLen*math.log(len(options), 2)


def makeNHypoth(seq, hypothLen, options=None):
    if options == None:
        options = set(seq)

    subSeqs = rollingSubsequences(seq, hypothLen)

    hypoth = {}
    for subSeq in set(subSeqs):
        hypoth[subSeq] = collections.Counter(options) #pretend every item was seen once to stop 1 or 0 probabilities (like laplace induction)

    for i in range(len(subSeqs[:-1])):
        hypoth[subSeqs[i]][subSeqs[i+1][-1]] += 1


    #normalize each prediction
    for prediction in hypoth.keys():
        total = sum(hypoth[prediction].values())
        for item in hypoth[prediction]:
            hypoth[prediction][item] /= total

    return hypoth


def solomonoffApprox(seq, maxHypothLen, options=None): #there's a good chance that i misunderstood solomonoff induction, but i'm pretty sure this does it on the set of hypotheses that give next observation predictions based on the n past observations, assigning predictions to next observations for every sequence of n-observes
    if options == None:
        options = set(seq)

    scoredHypoths = list(map(lambda hypothLen: {'hypothLen': hypothLen, 'hypoth': makeNHypoth(seq, hypothLen, options=options), 'score': scoreHypoth(seq, makeNHypoth(seq, hypothLen, options=options), hypothLen, options=options)}, range(1, maxHypothLen+1)))

    scoredHypoths.sort(key=lambda hypothWithScore: -hypothWithScore['score'])

    return scoredHypoths


def play():
    runningSeq = tuple([input()])
    while True:
        workingHypothAndMeta = solomonoffApprox(runningSeq, len(runningSeq))[0]
        prediction = workingHypothAndMeta['hypoth'][runningSeq[-workingHypothAndMeta['hypothLen']:]]
        print(f"\nWorking Hypothesis Len: {workingHypothAndMeta['hypothLen']}")

        runningSeq += tuple([input("Next: ")])
        try:
            score = math.log(prediction[runningSeq[-1]], 2)
        except ValueError:
            score = -math.inf

        print(f"\nPredicted: {prediction}, Score = {score}")
