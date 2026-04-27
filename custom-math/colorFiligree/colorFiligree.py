# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:56:20 2022

@author: Xela 
"""

import itertools

import numpy as np
from PIL import Image

from tqdm import tqdm


def filigreeBinary(bits):
    #yield ('0'*bits)

    alreadyOutputted = set()
    for startingBitsNum in range(1, bits+1):
        neededTrailingZeros = bits - startingBitsNum
        possibleStartingBitStrs = ( bin(i)[2:].zfill(startingBitsNum) for i in range(2**(startingBitsNum)) )

        thisIterBitStrs = tuple([possibleStartingBitStr + neededTrailingZeros*'0' for possibleStartingBitStr in possibleStartingBitStrs if (possibleStartingBitStr + neededTrailingZeros*'0') not in alreadyOutputted])
        yield thisIterBitStrs
        alreadyOutputted.update(thisIterBitStrs)


def getNextNodes(length, numDims): #this explores in order of lowest to highest taxicab distance of the {numDims}-dimensional hypercube of side length {length-1} [so that the highest coord number is {length-1}]
    length -= 1 #kludge to shift the length to go from (0, length-1) without having to actually find and change the relevant parts of this function

    total = (length+1)**numDims
    currentNodes = tuple([numDims*tuple([0])])
    yield currentNodes

    iters = 1
    while iters < total:
        nextNodes = set()
        for node in currentNodes:
            for dim in range(len(node)):
                if node[dim] + 1 > length:
                    continue
                nextNodes.add( (*node[:dim], node[dim] + 1, *node[dim+1:]) )

        nextNodes = tuple(nextNodes)

        yield nextNodes
        currentNodes = nextNodes
        iters += len(nextNodes)


def multiDimBinaryFiligreeSearch(bits, dims):
    singleAxisFiligrees = [list(filigreeBinary(bits))] * dims
    indiceSearchOrder = getNextNodes(bits, dims)

    for ambivalentIndices in indiceSearchOrder:
        for indices in ambivalentIndices:
            thisItersSearchForEachAxis = [singleAxisFiligrees[i][indices[i]] for i in range(len(indices))]
            yield itertools.product(*thisItersSearchForEachAxis)


def makeUniColorImage(color, height, width): #color is a binary 3-tuple
    color = [int(colorComponent, 2) for colorComponent in color]
    imageArr = np.full((height, width, 3), color, dtype='uint8')

    return Image.fromarray(imageArr)


def colorFiligreeImages(height, width):
    bits = 8
    dims = 3

    for ambivalentColorBinaries in multiDimBinaryFiligreeSearch(bits, dims):
        for colorBinary in ambivalentColorBinaries:
            yield makeUniColorImage(colorBinary, height, width)


colorIms = colorFiligreeImages(100, 100)

with tqdm(total=255**3) as pbar:
    i = 0
    for im in colorIms:
        im.save(f'uniColorIms/{i}-{(lambda color: f"{hex(color[0])[2:].zfill(2)}{hex(color[1])[2:].zfill(2)}{hex(color[2])[2:].zfill(2)}")(im.getpixel((0,0)))}.png', optimize=True)

        i += 1
        pbar.update()
        if i == 2000:
            break
