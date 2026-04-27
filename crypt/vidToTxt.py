# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 22:27:53 2020

@author: Xela
"""


import base64


mode = int(input('mode select: (0: encode, 1: decode) \n'))

if mode == 0:
   scFilename = input('source filename: \n')
   textFilename = input('text save name: \n')
   scFile = open(scFilename, "rb")
   text = base64.b64encode(scFile.read())
   scFile.close()

   textFile = open(textFilename, "wb")
   textFile.write(text)
   textFile.close()
else:
   textFilename = input('text filename: \n')
   endFilename = input('end filename: \n')

   textFile = open(textFilename, 'rb')
   text = base64.b64decode(textFile.read())
   textFile.close()

   endFile = open(endFilename, "wb")
   endFile.write(text)
   endFile.close()