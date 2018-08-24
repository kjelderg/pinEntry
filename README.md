# pinEntry

A proof of concept/performance test for a PIN system that uses multiple random symbols on each key.

Currently it provides a handful of functions and then goes through a sample workflow.

## Sample run output:
```
0 :  [6, 'red', 'H', 'i', 'diamond', '@']
1 :  [0, 'grey', 'I', 'a', 'semicircle', '#']
2 :  [2, 'orange', 'J', 'b', 'square', '!']
3 :  [3, 'indigo', 'E', 'c', 'pentagon', '*']
4 :  [8, 'violet', 'D', 'e', 'oval', '%']
5 :  [5, 'white', 'B', 'j', 'circle', ')']
6 :  [4, 'yellow', 'C', 'h', 'trefoil', '$']
7 :  [7, 'blue', 'A', 'd', 'triangle', '&']
8 :  [1, 'black', 'F', 'f', 'plus', '(']
9 :  [9, 'green', 'G', 'g', 'trapezoid', '^']
Please enter the array indices of your PIN: 807152
0 :  [6, 'grey', 'J', 'c', 'oval', ')']
1 :  [0, 'orange', 'E', 'e', 'circle', '$']
2 :  [2, 'indigo', 'D', 'j', 'trefoil', '&']
3 :  [3, 'violet', 'B', 'h', 'triangle', '(']
4 :  [8, 'white', 'C', 'd', 'plus', '^']
5 :  [5, 'yellow', 'A', 'f', 'trapezoid', '@']
6 :  [4, 'blue', 'F', 'g', 'diamond', '#']
7 :  [7, 'black', 'G', 'i', 'semicircle', '!']
8 :  [1, 'green', 'H', 'a', 'square', '*']
9 :  [9, 'red', 'I', 'b', 'pentagon', '%']
Please enter the array indices of your PIN: 895817
You selected  [1, 'red', 'A', 'a', 'circle', '!']
We should store  2cb7d2571fd2461a960f01dda6c4aaf1:45518be8e8dbfdf252788d316a285d49161a30d199cd3561735b3e58f8ccf99a
0 :  [2, 'green', 'E', 'e', 'plus', ')']
1 :  [1, 'red', 'A', 'd', 'diamond', '*']
2 :  [7, 'white', 'D', 'f', 'trefoil', '@']
3 :  [4, 'grey', 'H', 'b', 'triangle', '^']
4 :  [6, 'blue', 'I', 'g', 'circle', '&']
5 :  [8, 'violet', 'G', 'c', 'oval', '$']
6 :  [5, 'orange', 'B', 'j', 'trapezoid', '!']
7 :  [0, 'yellow', 'J', 'i', 'square', '(']
8 :  [3, 'indigo', 'C', 'h', 'pentagon', '%']
9 :  [9, 'black', 'F', 'a', 'semicircle', '#']
Please enter the array indices of your PIN: 111946
MATCH: The keys to the kingdom
The hashes object is consuming  2097384 b  and took 0:00:00.346497 to build.
MATCH: The keys to the kingdom
The search took 0:00:00.029534 to execute.
```

## Functions

### genKeypad(symbols)
This takes an OrderedDict of symbol categories mapped to lists of specific symbols and returns a representation of a keypad.  The lists should be of the same size, the number of keys in the keypad.  The keypad is a list of keys, each containing one symbol each from the several categories from the symbols dictionary.

### randomKeypad(symbols)
This randomizes the symbols dictionary and returns a keypad.

### verifyKeypad(symbols)
This returns a keypad altered from the default in such a way that a PIN entry here will map to a specific PIN.  This is a way for a workflow where a user sets their PIN.  The workflow would be a lot like the "Enter your password, reenter your password" workflow users are used to.  Note that to properly protect from mistyped PINs, the user would have to enter their PIN a third time.

### promptUser(keypad)
This prompts the user to enter a pin and returns a set of "pinPresses".  "PinPresses" is the list of the keys (each containing a number of symbols) that the user entered.

### comparePinPresses(pinPresses1, pinPresses2)
This compares two sets of "pinPresses", as one would get from the following condensed password-setting workflow:
```
comparePinPresses(
	promptUser(randomKeypad(symbols)),
	promptUser(verifyKeypad(symbols))
)
```

### checkPass(salt, passwordHash, pinPresses)
Given the salt and passwordHash of the user's password, determine if pinPresses was a valid PIN attempt.  This does so by checking each possible PIN corresponding to the pinPresses against the provided passwordHash.

This would be appropriate for local authentication where it is acceptable to expose the passwordHash.  

### generateHashes(salt, pinPresses)
Given the salt and a PIN attempt, generate all possible passwordHashes that this PIN attempt could represent.  This returns a set of these hashes.

The return value of this function would be appropriate to pass over an untrusted channel to an authentication agent.
