#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 15:34:43 2024

@author: Xela
"""


import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import timeit

from tqdm import tqdm


def init_tokens(text):
    base_tokens = [] #[a,b,c] means a is 0, b is 1, c is 2
    tokenized = []
    for char in text:
        if char not in base_tokens:
            base_tokens.append(char)
        
        tokenized.append(base_tokens.index(char))
    
    return tokenized, base_tokens

#!!!there are duplicates!
def merge_tokens(tokenized, tokens, previous_digrams=[], previous_digram_counts=[], previous_best_digram=[]): #note that this updates inplace.
    digrams = previous_digrams
    digram_counts = previous_digram_counts
    for i in range(len(tokenized)-1):
        digram = [tokenized[i], tokenized[i+1]]
        if previous_best_digram != []:
            if digram[0] not in previous_best_digram and digram[1] not in previous_best_digram:
                continue #e.g. if the new digram was ef, then the ab digrams doesn't need to be updated.
        if digram not in digrams:
            digrams.append(digram)
            digram_counts.append(1)
            
        digram_counts[digrams.index(digram)] += 1
    
    best_digram_count = 0
    for i in range(len(digram_counts)):
        digram_count = digram_counts[i]
        if digram_count > best_digram_count:
            best_digram_count = digram_count
            best_digram = digrams[i]
    
    if best_digram_count > 0:
        new_token_indice = len(tokens)
        tokens.append(best_digram)
        i = 0
        while i < len(tokenized)-1:
            digram = [tokenized[i], tokenized[i+1]]
            if digram == best_digram:
                tokenized[i] = new_token_indice
                tokenized.pop(i+1)
                
            i+=1
    
    return digrams, digram_counts, best_digram

def tokenize(text, tokens):
    tokenized = []
    for char in text:
        tokenized.append(tokens.index(char))
    
    nothing_merged = False
    while not nothing_merged:
        nothing_merged = True
        i = 0
        while i < len(tokenized) - 1:
            digram = [tokenized[i], tokenized[i+1]]
            if digram in tokens:
                tokenized[i] = tokens.index(digram)
                tokenized.pop(i+1)
                nothing_merged = False
                
            i+=1
    return tokenized
            
def basify_token(token, tokens): #not inplace
    if type(token) == list:
        return basify_token(token[0], tokens) + basify_token(token[1], tokens)
    elif type(token) == int:
        return basify_token(tokens[token], tokens)
    elif type(token) == str:
        return token
    
def basify_tokens(tokens):
    basified_tokens = []
    for i in range(len(tokens)):
        basified_tokens.append(basify_token(tokens[i], tokens))
    
    return basified_tokens

def make_bpe(text, token_count, pbar_off=False):
    tokenized, tokens = init_tokens(text)
    merge_count = token_count - len(tokens)
    
    digrams, digram_counts, best_digram = [], [], []
    for _ in tqdm(range(merge_count), disable=pbar_off):
        merge_tokens(tokenized, tokens, digrams, digram_counts, best_digram)
        #digrams, digram_counts, best_digram = merge_tokens(tokenized, tokens, digrams, digram_counts, best_digram)
        
    return tokenized, tokens
    

with open('romeo_and_juliet.txt') as f:
    text = f.read()
   
#test on text
#'''
token_count = 200
romeo_tokenized, tokens = make_bpe(text, token_count)
basified_tokens = basify_tokens(tokens)
hello_tokenized = tokenize("Hello, World!", tokens)
#'''

'''
#Compute plots for the parameter values
total_text = text
def time_bpe(total_text, text_length, token_count):
    text = total_text[:text_length]
    time = timeit.timeit("make_bpe(text, token_count, pbar_off=True)", setup="from __main__ import make_bpe", globals={'text':text, 'token_count':token_count}, number=1)
    return time

text_length = len(text)
token_counts = np.floor(np.linspace(70, 5000, num=100)).astype("int")
times = np.empty_like(token_counts)
with tqdm(total=len(token_counts)) as pbar:
    for i in range(len(token_counts)):
        token_count = token_counts[i]
        times[i] = time_bpe(text, text_length, token_count)
        pbar.update()
plt.plot(token_counts, times)
'''

'''
text_lengths = np.floor(np.logspace(1, np.log10(16000), num=3)).astype("int")
token_counts = np.floor(np.linspace(70, 2000, num=50)).astype("int")
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
X, Y = np.meshgrid(text_lengths, token_counts)
Z = np.empty_like(X)
with tqdm(total=len(text_lengths)*len(token_counts)) as pbar:
    for i in range(len(token_counts)):
        for j in range(len(text_lengths)):
            text_length = X[i,j]
            token_count = Y[i,j]
            Z[i,j] = time_bpe(text, text_length, token_count)
            pbar.update()
        
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
'''