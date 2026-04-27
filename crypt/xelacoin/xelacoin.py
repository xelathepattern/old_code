# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:26:45 2021

@author: Xela
"""

#NOTE: INCOMPLETE!!!!!!
import hashlib
import rsa

import json
import os

from random import getrandbits


'''
block structure: dict with keys [blockNumber, prevHash, miner, transList, state, nonce]

transList structure: list of dicts with keys[from, to, amount, signature]

signature structure: rsa.sign( json.loads({'from': fromAddress, 'to': toAddress, 'amount': amount}), privateKeyOfFromAddress, 'SHA-1' )

the addresses are the public keys
'''

#note: hashes are after getting the string out of the json. don't just hash the plain file, do hashlib.sha256(bytes(open('block.json', 'r').read(), 'utf-8')).hexdigest()
#note: the ints corresponding to keys include the "-----BEGIN RSA PUBLIC KEY-----" stuff as they are just pkcs format thrown into bytes then thrown into int
#note: signatures are stored as ints in the block, we must convert to bytes before using the verify function


rsaPublicKeyPkcsLength = 426 #corresponds to 2048 bit key. if key length changes, this can be computed by len(rsa.newkeys(keyLength, poolsize=8)[0].save_pkcs1())
rsaPrivateKeyPkcsLength = 1683 #same as public key but with [1] instead of [0]
sigLength = 256 #similar method
BLOCK_SIZE = 10 #in num of transactions
miningReward = 1
DIFFICULTY = 5


def keyToInt(key):
   return int.from_bytes(key.save_pkcs1(), 'little')


def intToKey(keyInt, publicOrPrivate):
   if publicOrPrivate == 'public':
      return rsa.PublicKey.load_pkcs1(keyInt.to_bytes(rsaPublicKeyPkcsLength, 'little'))
   elif publicOrPrivate == 'private':
      return rsa.PrivateKey.load_pkcs1(keyInt.to_bytes(rsaPrivateKeyPkcsLength, 'little'))


def blockHashValid(blockHash):
   if blockHash[:DIFFICULTY] == '0'*DIFFICULTY:
      return True
   else:
      return False


def hashBlock(block): #block is dumped json
   return hashlib.sha256(bytes(json.dumps(block), 'utf-8')).hexdigest()


def checkBlock(blockFilename, pastBlock):
   #there are three rules:
   #1. block has less than BLOCK_SIZE transactions
   #2. The claimed prev hash of block = the hash of prevBlock
   #3. State is consistent with trans and previous state
   #4. No overspending has occured
   #5. Each transaction's signature is valid
   #6. Proof of work is valid [Hash of block passes whatever blockHashValid implements (being ambigious so i can change my mind on what it does)]

   with open(blockFilename) as f:
      thisBlock = json.load(f)

   claimedTransList = thisBlock['transList']
   #Rule 1
   if len(claimedTransList) > BLOCK_SIZE:
      return False, 'Block Too Big'


   #Rule 2
   prevHash = hashBlock(pastBlock)

   claimedPrevHash = thisBlock['prevHash']

   if claimedPrevHash != prevHash:
      return False, 'Claimed prevHash is false', prevHash


   #Rule 3
   claimedState = thisBlock['state']

   pastState = pastBlock['state']

   realState = pastState
   for trans in claimedTransList:
      fromAddress = trans['from']
      toAddress = trans['to']
      amount = trans['amount']

      if fromAddress not in pastState.keys():
         return False, ['Nonexistent account attmempting to spend', fromAddress]

      realState[fromAddress] -= amount

      if toAddress in pastState.keys():
         realState[toAddress] += amount
      else:
         realState[toAddress] = amount


   miner = thisBlock['miner']
   if miner in pastState.keys():
      realState[miner] += miningReward
   else:
      realState[miner] = miningReward

   if claimedState != realState:
      return False, ['Claimed state is false', realState]


   #Rule 4
   for account in claimedState.keys():
      balance = claimedState[account]
      if balance < 0:
         return False, ['Overspending Detected', account, balance]


   #Rule 5
   for trans in claimedTransList:
      try:
         rsa.verify( json.dumps({'from': trans['from'], 'to': trans['to'], 'amount': trans['amount']}).encode(), trans['signature'].to_bytes(sigLength, 'little'), intToKey(int(trans['from']),'public') )
      except rsa.pkcs1.VerificationError:
         return False, ['Invalid signature detected', trans]


   #Rule 6
   if not blockHashValid(hashBlock(thisBlock)):
      return False, ['proof of work invalid', hashBlock(thisBlock)]


   #hey, all the rules passed!
   return True


def mine(block): #block is dumped json
   while blockHashValid(hashBlock(block)) == False:
      block['nonce'] = getrandbits(64)

   return block





#pastBlock = json.load(open('pastBlockchain.json'))[-1]
#print(checkBlock('block.json', pastBlock))

#timeit.timeit(stmt='xelacoin.mine(json.load(open(\'block.json\')))', setup='import json; import xelacoin')
