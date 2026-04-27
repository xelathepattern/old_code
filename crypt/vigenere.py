# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 16:39:41 2020

@author: Xela
"""


def numCon(string):

   #convert to numbers
   stringNum = []

   for letter in string:
      if ord(letter) == 32: #detect and encode spaces
         stringNum.append(32)
      else:
         stringNum.append(ord(letter.lower())-97)
   return stringNum


def encode(plain, key):

   #convert to num
   plainNum = numCon(plain)
   keyNum = numCon(key)
   #decode and strip spaces in key
   i = 0
   while i < len(keyNum):
      if keyNum[i] == 32:
         keyNum.pop(i)
      i += 1
   #encrypt
   i = 0
   keyLength = len(keyNum)
   cipherNum = []

   for num in plainNum:
      if num == 32: #pass spaces
         cipherNum.append(num)
      else:
         cipherNum.append((num + keyNum[i])%26)
         i = (i+1)%keyLength

   cipherText = ''

   for num in cipherNum:
      if num == 32: #decode and pass spaces
         cipherText += ' '
      else:
         cipherText += chr(num+97)

   return cipherText

def decode(cipher, key):

   #convert to num
   cipherNum = numCon(cipher)
   keyNum = numCon(key)

   #decode and strip spaces in key
   i = 0
   while i < len(keyNum):
      if keyNum[i] == 32:
         keyNum.pop(i)
      i += 1

   #decrypt
   i = 0
   keyLength = len(keyNum)
   plainNum = []

   for num in cipherNum:
      if num == 32: #pass spaces
         plainNum.append(num)
      else:
         plainNum.append((num - keyNum[i])%26)
         i = (i+1)%keyLength

   plainText = ''

   for num in plainNum:
      if num == 32: #decode and pass spaces
         plainText += ' '
      else:
         plainText += chr(num+97)

   return plainText

