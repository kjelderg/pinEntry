#!/usr/bin/python
from collections import OrderedDict
from datetime import datetime
import hashlib, itertools, random, sys, uuid

symbols = OrderedDict([
   ("numbers", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
   ("colors",  ["red", "orange", "yellow", "green", "blue", "indigo", "violet", "black", "white", "grey"]),
   ("uppers",  ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]),
   ("lowers",  ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]),
   ("shapes",  ["circle", "oval", "triangle", "square", "pentagon", "plus", "trapezoid", "diamond", "trefoil", "semicircle"]),
   ("symbols", ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"])
])

# create a keypad from the symbols dictionary
def genKeypad(s):
   keypad = []
   for i in range(0, len(s[next(iter(s))])):
      keypad.append([s[k][i] for k in s])
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
      i += 1

   return genKeypad(v)

# provide an interactive prompt for user PIN input.
#  return: the list of pinPresses
def promptUser(kp):
   for i,v in enumerate(kp):
      print i,": ",v
   return [kp[int(i)] for i in raw_input("Please enter the array indices of your PIN: ")]

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
   return set([
      hashlib.sha256(''.join(str(v) for v in p).encode()+s).hexdigest()
         for p in list(itertools.product(*pinPresses))
   ])

def checkPass(s, h, pinPresses):
   for p in list(itertools.product(*pinPresses)):
      if h == hashlib.sha256(''.join(str(v) for v in p).encode()+s).hexdigest():
         return True
   return False


# 1. Create a new user pin
first = promptUser(randomKeypad(symbols))# NOTE: this alters symbols
second = promptUser(verifyKeypad(symbols))

# 2. generate the real password hash
PIN = comparePinPresses(first, second)
print "You selected ", PIN
salt = uuid.uuid4().hex
passwordHash = hashlib.sha256(''.join(str(v) for v in PIN).encode()+salt).hexdigest()
print "We should store ", ''.join([salt, ":", passwordHash])

# 3. have the user make a password attempt
pinPress = promptUser(randomKeypad(symbols)) # NOTE: this alters symbols

# 4a. generate a list of all possible password hashes and then check that.  This is a common model for remote password checks.
#     NOTE: this is n^l hashes for n symbol types and an l-length PIN
start = datetime.now()
hashes = generateHashes(salt, pinPress)
if passwordHash in hashes:
   print "MATCH: The keys to the kingdom" 
else:
   print "MISMATCH: better luck next time."
print "The hashes object is consuming ", sys.getsizeof(hashes), "b", " and took {} to build.".format(datetime.now() - start)

# 4b. pass the password hash to the checking function.  This is a common model for a local password check.
start = datetime.now()
if checkPass(salt, passwordHash, pinPress):
   print "MATCH: The keys to the kingdom"
else:
   print "MISMATCH: better luck next time."
print "The search took {} to execute.".format(datetime.now() - start)

