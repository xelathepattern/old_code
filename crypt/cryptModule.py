from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename

import collections

import math
import random
import numpy as np

from tqdm import tqdm

import os, sys


def makeCharList(asciiCharsOnly = True, includeNewline = True, padToPrime=False):
    charList = []
    if includeNewline:
        charList += ['\n']

    if asciiCharsOnly: #no ascii-only guarantee when padding to prime
        charList += [chr(i) for i in range(32, 127)]
        #the nearest prime with these sizes is 97
        charList += [chr(161), chr(162)][:97-len(charList)]
    else:
        charList = [chr(i) for i in range(32, 127)] + [chr(i) for i in range(161, 5873)] + [chr(i) for i in range(7248, 55292)]

    return tuple(charList)


charList = makeCharList()


def numberify(text):
    return [charList.index(char) for char in text]


WORD_FILE = ""
wordList = []
with open(WORD_FILE) as f:
    wordList = f.read().split('\n')
for i in range(len(wordList)):
    wordList[i] = wordList[i].strip().lower()

wordList = set(wordList) #this speeds up checking if a word is in the wordList by a factor 1000!!!

FREQ_LIST = [' ', 'e', 't', 'a', 'r', 'i'] #part of the freqlist of a random wikipedia page
def makeFreqList():
    freqlist = collections.Counter(read_file()).most_common()
    freqlist = [freqlist[i][0] for i in range(len(freqlist))]


    return freqlist


def open_file():
    root = Tk()
    root.attributes('-topmost', True)
    filename = askopenfilename(filetypes=[("Text File", '.txt')], defaultextension='.txt')
    root.withdraw()
    return filename


def read_file(filepath=None):
    if not filepath:
        filepath = open_file()

    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    cleanedText = ''
    for char in text:
        if char in charList:
            cleanedText += char

    return cleanedText


def getSaveFileObject():
    root = Tk()
    root.attributes("-topmost", True)
    file = asksaveasfile()

    return file


def save_to_file(text):
    with open(asksaveasfilename(filetypes=[("Text File", '.txt')], defaultextension='.txt'), 'w', encoding='utf-8') as f:
        f.write(text)


def wordScore(text, sampleByPercentage=False, sampleByAmount=True, samplePercentage=.00001, sampleAmount=1000):
    words = text.split(' ')

    if sampleByPercentage:
        sampleAmount = max(1000, len(words)*samplePercentage)
    elif sampleByAmount:
        sampleAmount = sampleAmount

    sampleAmount = min(sampleAmount, len(words))
    samples = random.sample(words, sampleAmount)

    numOfRecognizedWords = 0
    for word in samples:
        word = word.lower().strip(' .,?!')
        if word in wordList:
            numOfRecognizedWords += 1


    return numOfRecognizedWords/len(samples)


def caesarEncrypt(plaintext, shift):
    ciphertext = ''
    for char in plaintext:
        ciphertext += charList[ (charList.index(char) + shift) % len(charList) ]

    return ciphertext


def caesarDecrypt(ciphertext, shift):
    return caesarEncrypt(ciphertext, -shift)


def askEncrypt(plaintext, writeToFileObject=None):
    shift = int(input("Input an integer key shift: "))

    if writeToFileObject:
        writeToFileObject.write(caesarEncrypt(plaintext, shift))
    else:
        return caesarEncrypt(plaintext, shift)


def askDecrypt(ciphertext, writeToFileObject=None):
    shift = int(input("Input an integer key shift: "))

    if writeToFileObject:
        writeToFileObject.write(caesarDecrypt(ciphertext, shift))
    else:
        return caesarDecrypt(ciphertext, shift)


def textToVals(text):
    return [ord(char) for char in text]


def caesarCrackDict(ctext):
    likelyKeysFreqs = {}
    for key in range(len(charList)):
        dtext = caesarDecrypt(ctext, key)
        dtextScore = wordScore(dtext)
        if dtextScore > 0:
            likelyKeysFreqs[key] = dtextScore*100

    sortedKeys = zip(likelyKeysFreqs.keys(), likelyKeysFreqs.values())
    sortedKeys.sort(reverse=True, key=lambda key: sortedKeys[1])
    return sortedKeys, list(map(lambda k: caesarDecrypt(ctext, k[0]), sortedKeys))


def caesarCrackFreq(ctext):
    letterFreqs = collections.Counter(ctext)
    currentMostFreq = ['', 0]
    for char in letterFreqs.keys():
        if letterFreqs[char] > currentMostFreq[1]:
            currentMostFreq[0] = char
            currentMostFreq[1] = letterFreqs[char]


    mostFreq = currentMostFreq[0]

    keyshifts = []
    for char in FREQ_LIST:
        keyshifts.append(charList.index(mostFreq) - charList.index(char))


    dtexts = list(map(lambda k: caesarDecrypt(ctext, k), keyshifts))
    keysWithScores = list(zip(keyshifts, map(wordScore, dtexts)))

    return keysWithScores, dtexts


def caesarCrack(ctext):
    return caesarCrackFreq(ctext)


def caesar(text, key, mode="encrypt"):
    if type(key) == str:
        numList = [charList.index(char) for char in key]
        key = sum(numList) % len(charList)

    if mode == "encrypt":
        return caesarEncrypt(text, key)
    elif mode == "decrypt":
        return caesarDecrypt(text, key)


def vigEncrypt(plaintext, keytext):
    shifts = [charList.index(char) for char in keytext]

    ciphertext = ''
    for i in range(len(plaintext)):
        ciphertext += charList[ (charList.index(plaintext[i]) + shifts[i%len(shifts)]) % len(charList) ]

    return ciphertext


def vigDecrypt(ciphertext, keytext):
    inverseShifts = [(len(charList)-charList.index(char))%len(charList) for char in keytext]
    inverseChars =  [charList[i] for i in inverseShifts]

    inverseKey = ''
    for char in inverseChars:
        inverseKey += char


    return vigEncrypt(ciphertext, inverseKey)


def vig(text, key, mode = 'encrypt'):
    if mode == "encrypt":
        return vigEncrypt(text, key)
    elif mode == "decrypt":
        return vigDecrypt(text, key)


def getNextNodes(numDims, length, currentNodes=None):
    #explore via a graph that spreads out
    #pickup where last left off
    if not currentNodes:
        return [numDims*[0]]

    #imagine a sidelength=length dims-d hypercube, searching in the lowest number regions first
    #this explores in order of lowest to highest taxicab distance
    nextNodes = []
    for node in currentNodes:
        for dim in range(len(node)):
            if node[dim] + 1 > length:
                continue
            nextNodes.append( [*node[:dim], node[dim] + 1, *node[dim+1:]] )


    return nextNodes


def vigCrackGivenLength(ciphertext, keyLength, tryBrute=True, endThreshold=.7, nextBatch=0, prevNodes=None, wordizeDText=False): #batch allows continuing where previously left off
    miniCipherTexts = []
    for miniCipher in range(keyLength):
        miniCipherTexts.append(ciphertext[miniCipher::keyLength])


    likelyMiniKeys = []
    for miniCipherText in miniCipherTexts:
        likelyMiniKeys.append(caesarCrackFreq(miniCipherText)[0]) #each element of likelyMiniKeys is a list of the likely minikeys in that position of the total key


    if tryBrute:
        bestScoringKey = [None, 0]
        try:
            batchIndices = range(nextBatch, len(FREQ_LIST)*keyLength) #max taxicab distance
            print("Cracking...")
            for indice in batchIndices:
                nextNodes = getNextNodes(keyLength, len(FREQ_LIST), currentNodes=prevNodes)
                for miniKeysIndex in tqdm(nextNodes):
                    thisKeyNums = []
                    for j in range(keyLength):
                        thisKeyNums.append(likelyMiniKeys[j][ miniKeysIndex[j] ])


                    thisKey = [charList[i[0]%len(charList)] for i in thisKeyNums]

                    thisScore = wordScore(vigDecrypt(ciphertext, thisKey))
                    if thisScore > bestScoringKey[1]:
                        key = ''
                        for char in thisKey: #stringify
                            key += char

                        print('\nCurrent Best Key: '+key)

                        bestScoringKey = [thisKey, thisScore]

                    if thisScore >= endThreshold:
                        key = ''
                        for char in bestScoringKey[0]: #stringify
                            key += char

                        if wordizeDText:
                            return  key, thisScore, wordize(vigDecrypt(ciphertext, key)), nextBatch, prevNodes
                        else:
                            return  key, thisScore, vigDecrypt(ciphertext, key), nextBatch, prevNodes


                nextBatch += 1

                prevNodes = nextNodes

        except KeyboardInterrupt: #return prematurely
           pass #intentional pass, as in just catch for the sake of stopping that for loop


        key = ''
        for char in bestScoringKey[0]: #stringify
            key += char

        if wordizeDText:
            return key, bestScoringKey[1], wordize(vigDecrypt(ciphertext, key)), nextBatch, prevNodes
        else:
            return key, bestScoringKey[1], vigDecrypt(ciphertext, key), nextBatch, prevNodes

    else:
        mostLikelyKeyNums = [likelyMiniKey[0] for likelyMiniKey in likelyMiniKeys]

        mostLikelyKey = [charList[i%len(charList)] for i in mostLikelyKeyNums]

        if wordizeDText:
            return mostLikelyKey, wordize(vigDecrypt(ciphertext, mostLikelyKey))
        else:
            return mostLikelyKey, vigDecrypt(ciphertext, mostLikelyKey)


def wordDistance(word1, word2, insertionWeight=2, substitutionWeight=1):
    biggest = word1 if len(word1)>len(word2) else word2
    otherWord = word1 if biggest==word2 else word2
    distance = 0

    for i in range(len(biggest)):
        if i >= len(otherWord):
            distance += insertionWeight
        elif biggest[i] != otherWord[i]:
            distance += substitutionWeight

    return distance


def closestWord(word1, stopEarlyThreshold=2):
    word1Clean = word1.strip(' .,?!')
    dirt = ''
    for char in word1:
        if char not in word1Clean:
            dirt += char

    word1Clean = word1Clean.lower()
    if word1Clean.isdigit() or word1Clean=='': #definitely not almost a word
        return [word1Clean, 0]

    if len(word1Clean) < 4: #abnormally short word
        stopEarlyThreshold = 0 #require the actual closest word

    firstIter = True
    isCapital = word1[0].isupper()
    for word2 in wordList:
        word2Clean = word2.lower().strip(' .,?!')
        if firstIter:
            firstIter = False
            closest = [word2Clean, wordDistance(word1Clean, word2Clean)]
        else:
            distance = wordDistance(word1Clean, word2Clean)
            if distance <= stopEarlyThreshold:
                closest = [word2Clean, distance]
                break
            elif distance < closest[1]:
                closest = [word2Clean, distance]

    closest[0] = closest[0].capitalize() if isCapital else closest[0]
    closest[0] += dirt

    return closest


def wordize(text, tooFarThreshold=4):
    words = text.split(' ')
    for i in tqdm(range(len(words))):
        if words[i] not in wordList:
            closest = closestWord(words[i])
            if closest[1] < tooFarThreshold: #if it's too far away from a word then it's probably not meant to be a word
                words[i] = closest[0]

    text = ''
    for word in words:
        text += word + ' '

    return text


def fixVigKey(ctext, key, dtext=None, bigThresh=5, obvThresh=1): #only does 1 correction
    if dtext==None:
        dtext = vigDecrypt(ctext, key)

    words = dtext.split(' ')

    wordsWithAbsoluteIndex = []
    i = 0
    for word in words:
        wordsWithAbsoluteIndex.append([word, i])
        i += len(word) + 1



    for wordWithAbsoluteIndex in wordsWithAbsoluteIndex:
        word = wordWithAbsoluteIndex[0].strip('.,!?')
        if len(word) > bigThresh: #big word means easier to tell where it's wrong
            closest = closestWord(word)
            if closest[1] <= obvThresh: #close word means the error is obvious
                correctWord = closest[0]

                biggest = correctWord if len(correctWord) > len(word) else word
                otherWord = word if biggest==correctWord else correctWord

                wrongRelativeIndex = None
                for i in range(len(biggest)):
                    if biggest[i] != otherWord[i]:
                        wrongRelativeIndex = i
                        break

                if wrongRelativeIndex == None:
                    return key, vigDecrypt(ctext, key)

                correction = (charList.index(word[wrongRelativeIndex]) - charList.index(correctWord[wrongRelativeIndex]))%len(charList)

                wrongAbsoluteIndex = wordWithAbsoluteIndex[1] + wrongRelativeIndex
                wrongKeyIndex = wrongAbsoluteIndex%len(key)

                correctedKey = ''
                for i in range(len(key)):
                    if i != wrongKeyIndex:
                        correctedKey += key[i]
                    else:
                        correctedKey += charList[(charList.index(key[i]) + correction)%len(charList)]


                return correctedKey, vigDecrypt(ctext, correctedKey)


def vigCrack(ctext, correctThreshold=.8):
    keyLen = kasiski(ctext)
    key, score, dtext = vigCrackGivenLength(ctext, keyLen)[:3]

    if score < correctThreshold:
        fixedKey, dtext = fixVigKey(ctext, key, dtext=dtext)
        score = wordScore(dtext)

        keyWithScore = [fixedKey, score]
    else:
        keyWithScore = [key, score]


    return [keyWithScore], [vigDecrypt(ctext, keyWithScore[0])]


def coincidenceIndex(text1, text2):
    coincidences = 0

    biggest = text1 if len(text1) > len(text2) else text2
    other = text2 if biggest==text1 else text1

    for i in range(len(other)):
        coincidences += (biggest[i] == other[i])

    return coincidences/(len(biggest)/95)


def offsetText(text, offset):
    return text[-offset:] + text[:-offset]


def gcd(numList):
    currentGCD = math.gcd(numList[0], numList[1])
    for num in numList[2:]:
        currentGCD = math.gcd(currentGCD, num)

    return currentGCD


def kasiski(ctext, coincidenceThreshold=6, earlyKeysStopThresh=5):
    possibleKeyLens = []
    print("Performing kasiski examination...")
    for offset in tqdm(range(1, len(ctext) + 1)):
        if len(possibleKeyLens) >= earlyKeysStopThresh:
            break

        thisCoincidenceIndex = coincidenceIndex(ctext, offsetText(ctext, offset))

        if thisCoincidenceIndex > coincidenceThreshold:
            possibleKeyLens.append(offset)

    keyLen = gcd(possibleKeyLens)
    print(f"Key Length: {keyLen}")

    return keyLen


def streamEncrypt(ptext, password):
    random.seed(password)
    ctext = ''
    for char in ptext:
        ctext += vigEncrypt(char, random.choice(charList))

    return ctext


def streamDecrypt(ctext, password):
    random.seed(password)
    ptext = ''
    for char in ctext:
        ptext += vigDecrypt(char, random.choice(charList))

    return ptext


def stream(text, key, mode = "encrypt"):
    if mode == "encrypt":
        return streamEncrypt(text, key)
    elif mode == "decrypt":
        return streamDecrypt(text, key)


def hillEncrypt(plaintext, key):
    charList = makeCharList(padToPrime=True)

    blockLength = len(key)**.5

    if not blockLength.is_integer():
        key += ' ' * ( (math.floor(blockLength)+1)**2 - len(key) ) #pad it
    key = list(key)

    blockLength = len(key)**.5
    blockLength = int(blockLength)

    messagePaddingAmount = blockLength - len(plaintext)%blockLength
    if len(plaintext)%blockLength != 0:
        plaintext += ' ' * (messagePaddingAmount) #pad plaintext


    vectors = []
    for i in range(len(key)//blockLength):
        vectors.append(key[i*blockLength:(i+1)*blockLength])

    for i in range(len(vectors)):
        for j in range(len(vectors[i])):
            vectors[i][j] = charList.index(vectors[i][j])


    keyOperator = np.array(vectors)

    plaintext = list(plaintext)
    plainVectors = []
    for i in range(len(plaintext)//blockLength):
        plainVectors.append(np.array( [charList.index(char) for char in plaintext[i*blockLength:(i+1)*blockLength]] ))


    cipherVectors = []
    for vector in plainVectors:
        cipherVectors.append(keyOperator @ vector)


    flattenedCipherVectors = [num for vector in cipherVectors for num in vector] #apparently you can nest list comprehensions.

    #do mods and stringify
    ciphertext = ''
    for num in flattenedCipherVectors:
        ciphertext += charList[num%len(charList)]

    return ciphertext


def hillDecrypt(ciphertext, key):
    charList = makeCharList(padToPrime=True)

    blockLength = len(key)**.5
    if not blockLength.is_integer():
        key += ' ' * ( (math.floor(blockLength)+1)**2 - len(key) ) #pad it
    key = list(key)

    blockLength = len(key)**.5
    blockLength = int(blockLength)

    vectors = []
    for i in range(len(key) // blockLength):
        vectors.append(key[i * blockLength:(i + 1) * blockLength])

    for i in range(len(vectors)):
        for j in range(len(vectors[i])):
            vectors[i][j] = charList.index(vectors[i][j])

    keyOperator = np.array(vectors)
    #we want the inverse mod len(charList)
    realInverseKeyOperator = np.linalg.inv(keyOperator)
    det = int(round(np.linalg.det(keyOperator)))
    #inverseOverReals * det = cofactor matrix * modInverseOfDet = inverseOverMod
    inverseKeyOperator = realInverseKeyOperator * det * pow(det%len(charList), -1, len(charList))


    for i in range(len(inverseKeyOperator)):
        for j in range(len(inverseKeyOperator)):
            inverseKeyOperator[i][j] %= len(charList)


    inverseKeyVectors = []
    for vector in inverseKeyOperator:
        inverseKeyVectors.append(vector)


    flattenedInverseKeyVectors = [num for vector in inverseKeyVectors for num in vector] #flatten once

    #do mods and stringify
    inverseKey = ''
    for num in flattenedInverseKeyVectors:
        inverseKey += charList[round(num)%len(charList)]

    return hillEncrypt(ciphertext, inverseKey)


def hill(text, key, mode = "encrypt"):
    if mode == "encrypt":
        return hillEncrypt(text, key)
    elif mode == "decrypt":
        return hillDecrypt(text, key)


def affineEncrypt(ptext, key):
    if len(key) > 2:
        key = [charList.index(char) for char in key]

        firstHalf = key[:len(key)//2]
        secondHalf = key[len(key)//2:]

        a = sum(firstHalf)
        b = sum(secondHalf)
    else:
        a = charList.index(key[0])
        b = charList.index(key[1])

    ctext = ''
    for char in ptext:
        ctext += charList[(a*charList.index(char) + b)%len(charList)]

    return ctext


def affineDecrypt(ctext, key):
    if len(key) > 2:
        key = [charList.index(char) for char in key]

        firstHalf = key[:len(key)//2]
        secondHalf = key[len(key)//2:]

        a = sum(firstHalf)
        b = sum(secondHalf)
    else:
        a = charList.index(key[0])
        b = charList.index(key[1])

    aInverse = pow(a, -1, len(charList))
    bInverse = -b

    ptext = ''
    for char in ctext:
        ptext += charList[aInverse*(charList.index(char) + bInverse)%len(charList)]

    return ptext


def affine(text, key, mode = "encrypt"):
    if mode == "encrypt":
        return affineEncrypt(text, key)
    elif mode == "decrypt":
        return affineDecrypt(text, key)


def nthConcatenation(base, n):
    #print([(base**i)*(base-1) for i in range(n)])
    return sum([(base**i)*(base-1) for i in range(n)])


def textToBaseNum(text): #gets the base 10 representation of the ptext interpreted as a base charList number
    return sum([(len(charList)**i)*(charList.index(text[i])) for i in range(len(text))])


def baseNumToText(baseNum):
    base = len(charList)

    bDigits = []
    running = baseNum
    iteratingRange = list(range(int(math.log(baseNum, base)) + 1)) #doing this so we can reverse
    iteratingRange.reverse()
    for i in iteratingRange:
        bDigits.append(running//(base**i))
        running = baseNum%(base**i)


    text = ''
    bDigits.reverse()
    for digit in bDigits:
        text += charList[digit]

    return text


def expEncrypt(ptext, e, p=3037): #!!!fix this!
    if type(e) == str:
        e = sum([charList.index(char) for char in e])%len(charList)

    if math.gcd(e, p-1) != 1:
        print("Can't invert!")

    base = len(charList)
    currentN = 0
    while nthConcatenation(base, currentN) < p:
        currentN += 1

    currentN -= 1

    blockLength = currentN
    #print(blockLength)

    if not (len(ptext)%blockLength == 0): #pad the ptext
        ptext += " " * (blockLength - len(ptext)%blockLength)

    blocks = []
    for i in range(len(ptext)//blockLength):
        blocks.append(ptext[i*blockLength:(i+1)*blockLength])

    #print(blocks)
    blocks = [textToBaseNum(block) for block in blocks] #turn the blocks into numbers
    #print(blocks)

    cNums = []
    for block in blocks:
        cNums.append(pow(block, e, p))
    #print(cNums)

    ctext = ''
    for num in cNums:
        ctext += baseNumToText(num)


    return ctext


#print(expEncrypt("Hello", 13))

def expDecrypt(ctext, e, p=3037):
    if type(e) == str:
        e = sum([charList.index(char) for char in e])%len(charList)

    if math.gcd(e, p-1) != 1:
        print("Can't invert!")

    d = pow(e, -1, p-1)

    return expEncrypt(ctext, d)


def exp(text, e, mode='encrypt', p=3037): #!!! test this!
    if mode=='encrypt':
        return expEncrypt(text, e, p=p)
    elif mode=='decrypt':
        return expDecrypt(text, e, p=p)


def graphicalCrypt(func, mode):
    intext = read_file()
    key = input("Password: ")
    outtext = func(intext, key, mode)
    save_to_file(outtext)


def graphicalCrack(func):
    ctext = read_file()

    sortedKeys, likelyPTexts = func(ctext)[:2]
    for key in sortedKeys:
        print(f"Key: {key[0]} : {key[1]}")

    for ptext in list(likelyPTexts):
        print()
        printNext = input("Print next? (enter=yes)")
        if printNext != '':
            break
        print()
        print(ptext[:500])

        toSave = input("\nSave? (y/n)")
        if toSave == "y":
            save_to_file(ptext)


def generateMenuStr(cipherNames, crackableNames):
    menuStr = "Menu:\n"
    choiceMap = {}
    i = 1
    for name in cipherNames:
        for option in ['encrypt', 'decrypt']:
            numberOfSpaces = 4 - (len(str(i))-1)
            spaces = " " * numberOfSpaces
            menuStr += f"{spaces}{i}. {name.capitalize()} {option.capitalize()}\n"
            choiceMap[i] = f"{name}, '{option}'"
            i += 1

        if name in crackableNames:
            menuStr += f"{spaces}{i}. {name.capitalize()} Crack\n"
            choiceMap[i] = name + "Crack"
            i += 1


    numberOfSpaces = 4 - (len(str(i))-1)
    spaces = " " * numberOfSpaces
    menuStr += f"{spaces}{i}. Custom Chain\n"
    choiceMap[i] = "chain"
    i += 1


    numberOfSpaces = 4 - (len(str(i))-1)
    spaces = " " * numberOfSpaces
    menuStr += f"{spaces}{i}. Quit\n\nChoice: "
    choiceMap[i] = "Quit"

    return menuStr, choiceMap


def chain(chainList, text, keyList, encryptOrDecrypt='encrypt'):
    if encryptOrDecrypt == 'decrypt':
        chainList.reverse()

    i=0
    for cipher in chainList:
        text = eval(f"{cipher}(text, keyList[i], encryptOrDecrypt)")
        i += 1

    return text


if __name__ == "__main__":
    repeat = True
    while repeat:
        CIPHER_LIST = ['caesar', "vig", "stream", "hill", 'affine', 'exp']
        CRACKABLE_LIST = ['caesar', 'vig']
        ABBREVIATIONS_LIST = ['c', 'v', 's', 'h', 'a', 'e']

        chainAbbreviations = {}
        for i in range(len(ABBREVIATIONS_LIST)):
            chainAbbreviations[ABBREVIATIONS_LIST[i]] = CIPHER_LIST[i]

        menu, choiceMap = generateMenuStr(CIPHER_LIST, CRACKABLE_LIST)
        print("Exp not done yet")
        choice = choiceMap[int(input(menu))]

        if choice == "Quit":
            repeat = False

        elif choice == "chain":
            chainEmbeddedInKey = input("Get chain from key? (y/n): ") == 'y'

            if chainEmbeddedInKey:
                rawKey = input("Key: ")

                rawChain = rawKey.split('_')[0]
                keyList = [rawKey[len(rawChain)+1:]] * len(rawChain)

                chainList = []
                for char in rawChain:
                    chainList.append(chainAbbreviations[char])



            else:
                chainList = input("Type Chain: ").split(' ')
                useDifferentKeys = input("Use Different Keys? (y/n): ") == 'y'

                if useDifferentKeys:
                    keyList = []
                    for i in range(len(chainList)):
                        keyList.append(input(f"Password {i+1}: "))
                else:
                    key = input("Password: ")
                    keyList = [key] * len(chainList)


            encryptOrDecrypt = "encrypt" if input("Encrypt or Decrypt? (encrypt/decrypt): ") == 'encrypt' else "decrypt"


            intext = read_file()

            outtext = chain(chainList, intext, keyList, encryptOrDecrypt=encryptOrDecrypt)

            save_to_file(outtext)

        else:
            if "Crack" in choice:
                exec(f"graphicalCrack({choice})")
            else:
                exec(f"graphicalCrypt({choice})")
