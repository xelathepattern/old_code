# -*- coding: utf-8 -*-
"""
Created on Sun Nov 1 19:50:26 2020

@author: Xela
"""


from numpy import array, zeros, uint8, tile, average

from PIL import Image
Image.MAX_IMAGE_PIXELS = None

from math import ceil


def split(text, n):

   #inspired by stackoverflow answer
	return [text[i:i+n] for i in range(0, len(text), n)]


def colorize(text, m_pretty=False):

   #get hex values of text
   textHex = ""
   for char in text:
      textHex += hex(ord(char))[2:]

   #split into color blocks
   colorList = split(textHex, 6)


   #every char corresponds to 2 hex digits
   #every 2 hex digits corresponds to 1 color component (R, G, or B)
   #we don't want the residue, we want what needs to be added to the residue to get a full color
   #therefore take the complement
   #except if the residue is 0, we don't want padding=3, we want padding=0, so we take the mod3 again
   padding = (3 - (len(textHex)//2) % 3) % 3

   #pad right of last block to color
   colorList[-1] = colorList[-1].ljust(6, '0')
   #add another block with amount of padding, and fill the left with 0's
   #to make it a color.
   colorList.append(hex(padding)[2:].zfill(6))

   if m_pretty == True:
      prettyOut = ""
      for color in colorList:
         #formatted to make tatsuing the colors easy
         prettyOut += '#' + color + ' '

      return prettyOut
   else:
      return colorList


def rgb(hexList):

   rgbList = []
   for h in hexList:
      #it's a oneliner that splits by 2 and converts to int
      rgbList.append(list(int(component, 16) for component in split(h, 2) ) )

   return rgbList


def imagerize(text, pixelPerColor=100, percentOfWidth=.25, bMinMax=140, m_average=False):

   #bMinMax is the minimum maximum brightness of image

   #1 indice is just to get colorList to feed into rgb()
   rgbList = rgb(colorize(text))

   #colors are all very dark, so figure out
   #how much brighter it can be and then what
   #it should be to look pretty.
   #take the max to make sure we don't max out
   #the colors. 140 is the chosen brightness
   tmp = bMinMax - array(rgbList).max()
   bMod = tmp if tmp > 0 else 0
   #bMod info gets put into padding at the end, no need to append.


   #arrays go height,width,rgb. this is just width, rgb. it
   #fills with 8bit 0's to start with.
   plainData = zeros( (len(rgbList) * pixelPerColor, 3), dtype=uint8 )

   #make the width color data
   i = 0
   for color in rgbList:


      for j in range(pixelPerColor):
         plainData[i] = color #at width indice, make it = color
         i += 1



   #make height of image
   #round up so that percentOfWidth=0 corresponds to height of 1
   height = ceil(len(plainData)*percentOfWidth)
   #duplicate the width data down to the height
   #keep height and rgb same, tile across height
   data = tile(plainData, (height,1,1))

   #make the image brighter.
   data += bMod

   img = Image.fromarray(data)

   if m_average == True:
      #average the rgb values of the width along the first height
      #since the data is same across height, just average across the first
      #it returns a list containing the average color, so get it with [0]
      averageColor = list(average(array(img), axis=0)[0])

      return averageColor
   else:
      return img


def texterize(img, pixelPerColor=100, m_b=True):

   #load PIL image to np
   #hotfix feb 9 2021: for some reason it now appears that numpy puts 255 to the right of the rgb
   data = array(img)[:,:,:3]

   #second indice traverses along width, just take the first
   #height since it's identical along the rest.
   rgbList = data[0][::pixelPerColor]


   if m_b == True:
      #i made a goof in imagerize() that means that i added bMod to the rgb
      #values of bMod. it's easier to use this to make stuff work than to
      #work out how to correct it. correcting at the source would also be a
      #kerfuffle with how it's all set up. Now that i think about it,
      #it's not a bug, it's a feature.

      #Since the padding color is [0,0,padding], after applying bMod we get
      #[bMod,bMod,padding].
      bMod = rgbList[-1][0]

      #undo bMod(we needed to keep rgbList as an array so we could do this)
      rgbList -= bMod


   padding = rgbList[-1][2]

   #make rgbList live up to its name
   rgbList = list(rgbList)

   #we're finished with padding/brightness, throw it away.
   rgbList.pop()

   #get hexList
   hexList = []
   for i in rgbList:
      for j in i:
         hexList.append(hex(j)[2:])

   #undo padding
   #go to last indice, and then for every padding block go down an indice,
   #thus removing the same amount of blocks as there is padding.
   #(the slice doesn't include the ending indice, but gives nothing if end
   #=-0. since nothing should happen with 0 padding, just only do the removal
   #if there was padding
   if padding != 0:
      hexList = hexList[:(-1 * padding)]

   text = ''
   for i in hexList:
      text += chr(int(i, 16))

   return text




def test(testText, verbose=False):
   a=imagerize(testText)
   b=texterize(a)
   c=imagerize(b)
   if verbose:
      return a==b, array(a), b, array(c)
   else:
      return a==b



#useful stuff with PIL img:
#img.show()
#img.save('filename.png')
#Image.open('filename.png')
#np.array(img)