# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:10:53 2020

@author: Xela
"""

#version = 2.0


from midiutil.MidiFile import MIDIFile
from datetime import datetime


def init(bpm):
   song = MIDIFile(1)
   song.addTrackName(0,0,"Track 1")
   song.addTempo(0,0,bpm)

   return song

#TODO: use argument for sequential vs simultaneous vs manual
#(just a matrix of each note, where each note is a list of pitch, time, and duration)
def addNotes(song, notes, startTime, silence=True):
   #a note is (pitch, duration)
   for note in notes:
      pitch = note[0]
      duration = note[1]

      if silence and (pitch == 0):
         pass
      else:
         #song.addNote(track, channel, pitch, time + i, duration, volume)
         song.addNote(0,0,pitch,startTime,duration,100)

      startTime += duration

   return startTime


#C4=60, 12+C4=C5, 12+C5=C6, etc.
def numNote(numList):
   conv = {0:0,1:72,\
           2:74,3:76,4:77,5:79,6:81,7:83}

   noteList = []
   for i in numList:
      noteList.append( [ conv[int(i)], 1 ] )

   return noteList


def textNote(text):
   #95-32 (len=64)
   noteList = []
   for i in text:
      noteList.append([ord(i), 1])

   return noteList




def save(song,filename):
   with open(filename,'wb') as f:
      song.writeFile(f)


def uqname():
   return 'outMidi-' + str(datetime.now()).replace(' ','-').replace(':','-') + '.midi'




def numSong(song, numList):
   addNotes(song, numNote(numList), 0)

   return song


def textSong(song, text):
   addNotes(song, textNote(text), 0, silence=False)

   return song


def solresolToNums(text):
    i = 0
    numDict = {'do':1, 're':2, 'mi':3, 'fa':4, 'so':5, 'la':6, 'ti':7, 'si':7}
    numList = []
    while i < len(text):
        if text[i:i+3].lower() == 'sol':
            numList.append(5)
            i += 3
        elif text[i] == ' ':
            numList.append(0)
            i += 1
        elif text[i:i+2].lower() in numDict.keys():
            numList.append(numDict[text[i:i+2].lower()])
            i += 2
        else:
            i += 1

    numList.append(0)
    return numList


def solresolToSong(song, text):
    song = numSong(song, solresolToNums(text))

    return song
