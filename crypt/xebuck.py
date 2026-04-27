# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 18:59:19 2020

@author: Xela
"""

import hashlib
import sys


#hash function
def sha512(message):
  return hashlib.sha512(message.encode("UTF-8")).hexdigest()

#TODO return prints into return values
#used: 100-101
def truncId(denom, serialNum, security=16):
   #get secret
   f = open("secret thing.txt", "r")
   secret = f.read()
   f.close()


   #get user's claim
   claim = str(denom) + ':' + str(serialNum)

   #check if num is used
   f = open("used serial numbers.txt")

   f_contents = f.read()
   used_nums = f_contents.splitlines()
   for i in used_nums:
      if i == serialNum:
         print("Used serial number")
         sys.exit()

   f.close()


   #truncate id
   trunc_id = sha512(claim+secret)[:security]

   return trunc_id


#TODO turn prints into return values
def check(denom, serialNum, claim_id, security=16):
   trunc_id = truncId(denom, serialNum, security)

   if trunc_id == claim_id:
       print("Authorized")

       #write num to file
       f = open("used serial numbers.txt", "a")
       f.write(serialNum + "\n")
       f.close()
   else:
       print("Unauthorized")


#TODO read claimed serial numbers from a file
#TODO set stuff up so that claimed nums, secret password can be passed to the functions


