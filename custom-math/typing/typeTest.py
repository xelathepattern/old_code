# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 19:49:26 2022

@author: Xela
"""


from datetime import datetime
import time # != datetime.time

import random

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import itertools


with open('dictionary.txt') as f:
    WORD_SET = set(f.read().split('\n'))

with open('word_freqs.txt') as f:
    WORD_FREQS = pd.read_csv(f)

WORD_FREQS['Count'] /= WORD_FREQS['Count'].sum()
WORD_FREQS["Count"] = list(itertools.accumulate(WORD_FREQS["Count"]))

def testOnStr(testWords):
    testString = ''
    for word in testWords[:-1]:
        testString += word + ' '

    testString += testWords[-1] #so last word not followed by space

    print(f"{testString}")

    startT = time.time()
    _ = input()
    stopT = time.time()

    elapsedT = stopT - startT
    wpm = round((len(testString)/elapsedT)*(60/5), 2)
    with open('results.csv', 'a') as f:
        f.write(f"\n{stopT}, {wpm}")

def weightedSample():
    num = random.random()
    return WORD_FREQS.loc[WORD_FREQS.loc[num <= WORD_FREQS["Count"]]["Count"].idxmin()].Word

def performTest(difficulty, testLen, weight=True):
    if not weight:
        sameLengthWords = set({})
        for word in WORD_SET:
            if len(word) == difficulty:
                sameLengthWords.add(word)

        sameLengthWords = tuple(sameLengthWords)
        testWords = random.sample(sameLengthWords, testLen)
    else:
        testWords = [weightedSample() for _ in range(testLen)]

    testOnStr(testWords)


def log_fit(x, x_offset, y_offset, scale):
    with np.errstate(divide='ignore', invalid='ignore'):
        result = scale * np.log10(x - x_offset) + y_offset
        result = np.where(result >= 0, result, 0)
    return result

data = pd.read_csv('results.csv', comment='#').to_numpy()
time0Anchor = data[0,0]
data[:,0] -= time0Anchor
data[:,0] /= 3600*24

p0 = [-2, 0, 20/np.log10(2)] 
bounds = [[-10, -np.inf, 0], [-.1, np.inf, np.inf]]
out = sp.optimize.curve_fit(log_fit, data[:,0], data[:,1], p0=p0, bounds=bounds)
x_offset, y_offset, scale = out[0]

fit_plot_n = 100
day_start = data[0,0] - 10
day_end = data[-1,0]
fit_plot_xs = np.linspace(day_start, day_end, fit_plot_n)
preds = log_fit(fit_plot_xs, x_offset, y_offset, scale)

fig, ax = plt.subplots()
ax.plot(data[:,0], data[:, 1], '.', label='data')
ax.plot(fit_plot_xs, preds, label=f'log_fit: {scale:.2f} * log_10(x - {x_offset:.2f}) + {y_offset:.2f}')

ax.legend()

ax.set_xlabel(f'Days since {datetime.utcfromtimestamp(time0Anchor).strftime("%B %d, %Y")}')
ax.set_ylabel("WPM")

fig.savefig('results_plot.png')
