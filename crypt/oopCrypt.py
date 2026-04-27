# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 14:10:52 2022

@author: Xela 
"""

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename


class Cipher:
    def __init__(self):
        self.charList = [chr(i) for i in range(32, 127)]
        self.charModulo = len(self.charList)


    def clean(self, text):
        cleanedText = ''
        for char in text:
            if char in self.charList:
                cleanedText += (char)

        return cleanedText


    def getKey(self):
        while True:
            key = input("Key: ")

            if key == '':
                print("Key cannot be empty string!")
                continue

            cleanedKey = self.clean(key)

            if cleanedKey == key:
                return cleanedKey
            else:
                print(f"Invalid Key! Did you mean: {cleanedKey}")


    def charVals(self, text):
        return [self.charList.index(char) for char in text]


    def valChars(self, nums):
        return [self.charList[num] for num in nums]


    def get_filename(self):
        root = Tk()
        root.attributes('-topmost', True)
        print('select file to open')
        filename = askopenfilename(filetypes=[("Text File", '.txt')], defaultextension='.txt')
        root.withdraw()
        return filename

    def read_file(self, filepath=None):
        if not filepath:
            filepath = self.get_filename()

        with open(filepath, encoding='utf-8') as f:
            text = f.read()

        cleanedText = self.clean(text)

        return cleanedText

    def save_to_file(text):
        print('select file to save')
        with open(asksaveasfilename(filetypes=[("Text File", '.txt')], defaultextension='.txt'), 'w', encoding='utf-8') as f:
            f.write(text)



class Caesar(Cipher):
    def __init__(self, key=None):
        super(Caesar, self)

        if key == None:
            self.key = self.getKey()
        else:
            self.key = key


    def encrypt(self, text, key=None):
        plainNums = self.charVals(text)

        if not key==None:
            keyNums = self.charVals(self.key)
        else:
            keyNums = self.charVals(key)


        summedKey = sum(keyNums) % self.charModulo
        cipherNums = [(plainNum + summedKey) % self.charModulo for plainNum in plainNums]

        cipherText = self.valChars(cipherNums)

        return cipherText


    def decrypt(self, text): #!!! finish this
        keyNums = self.charVals(self.key)
        summedKey = sum(keyNums) % self.charModulo
        inverseKey = self.charModulo - summedKey
