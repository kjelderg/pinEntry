#!/usr/bin/python
from collections import OrderedDict
from datetime import datetime
import hashlib, itertools, random, sys, uuid

symbols = OrderedDict()
symbols["numbers"] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
symbols["colors"]  = ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "black", "white", "grey"]
symbols["uppers"]  = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
symbols["lowers"]  = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
symbols["shapes"]  = ["circle", "oval", "triangle", "square", "pentagon", "plus", "trapezoid", "diamond", "trefoil", "semicircle"]
symbols["symbols"] = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]

# create a keypad from the symbols dictionary
def genKeypad(s):
   keypad = []
   for i in range(0, len(s[next(iter(s))])):
      key = []
      for k in s:
         key.append(s[k][i])
      keypad.append(key)
   return keypad

# create a random keypad from the symbols dictionary
#  NOTE: this alters its input.
def randomKeypad(s):
   for k in s:
      random.shuffle(s[k])
   return genKeypad(s)
   

# create a keypad that will allow the user to verify a unique PIN
#  the key is ensuring that no symbol combinations are repeated on between the two keypads.
#  XXX: for our first implementation, we will just rotate the symbols forward.
def verifyKeypad(s):
   v = OrderedDict()

   i = 0
   for k in s:
      v[k] = s[k][i:] + s[k][:-i] if i else s[k]
      i = i + 1

   return genKeypad(v)

def promptUser(kp):
   for i,v in enumerate(kp):
      print i, ": ", v
   
   pinPress = raw_input("Please enter the array indices of your PIN: ")

   keys = []
   for i in pinPress:
      keys.append(kp[int(i)])

   return keys

# given two pin entries (a la verifyKeypad()), return the PIN
#  XXX: this probably breaks if multiple pins are possible.
#  NOTE: we do not compare mismatched lengths.
def comparePinPresses(a, b):
   if(len(a) != len(b)):
      return

   pin = []
   for i in range(0, len(a)):
      d = None
      for v in a[i]:
         if(v in b[i]):
            d = v
            break

      if d == None:# this is bad business, a mismatched PIN entry.
         return

      pin.append(d)
   return pin

def generateHashes(s, pinPresses):
   hashes = set()
   for p in list(itertools.product(*pinPresses)):
      hashes.add(s + ":" + hashlib.sha256(''.join(str(v) for v in p).encode()).hexdigest())
   return hashes


# 1. Create a new user pin
keypad = randomKeypad(symbols) # NOTE: this alters symbols
first = promptUser(keypad)
print first

keypad = verifyKeypad(symbols)
second = promptUser(keypad)
print second

# 2. generate the real password hash
PIN = comparePinPresses(first, second)
print "You selected ", PIN
salt = uuid.uuid4().hex
hash = salt + ":" + hashlib.sha256(''.join(str(v) for v in PIN).encode()).hexdigest()
print "Your hash is ", hash

# 3. have the user make a password attempt
keypad = randomKeypad(symbols) # NOTE: this alters symbols
pinPress = promptUser(keypad)
print pinPress

# 4. generate a list of all possible password hashes
#     NOTE: this is n^l hashes for n symbol types and an l-length PIN
start = datetime.now()
hashes = generateHashes(salt, pinPress)
print "The hashes object is consuming ", sys.getsizeof(hashes), "b"
print " and took {} to build.".format(datetime.now() - start)

# 5. report success
print "The keys to the kingdom: ", hash if hash in hashes else "better luck next time."
