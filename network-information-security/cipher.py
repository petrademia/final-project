# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from operator import xor
import binascii

def int2bin(i):
    if i == 0: return "0"
    s = ''
    while i:
        if i & i == 1:
            s = "1" + s
        else:
            s = "0" + s
        i /= 2
    return s

def bin2int(i):
    decimal = 0
    for digit in i:
        decimal = decimal*2 + int(digit)
    return decimal

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def num_digits(n):
    count = 0
    while n > 0:
        if n == 0:
            count += 1
        count += 1
        n = n/10
    return count

def numLen(num):
    return len(str(abs(num)))

def modulus64(x):
    s = 0 # the sum

    while x > 0: # get the digits
        s += x & (2**64-1)
        x >>= 64

    if s > 2**64:
        return modulus64(s)
    elif s == 2**64:
        return 0
    else:
        return s

def encrypt(binaryPlainText, binaryKey):
    #print "binaryPlainText: ", binaryPlainText
    #print "binaryKey:", binaryKey
    
    firstKey = []
    secondKey = []
    
    for i in range(0, len(binaryKey)):
        if i <= 3:
            firstKey.append(binaryKey[i]);
        else:
            secondKey.append(binaryKey[i]);
                            
    #print "First Key: ", firstKey
    #print "Second Key: ", secondKey
    
    fourHorsemen = len(binaryPlainText)/4
    leftHorsemen = len(binaryPlainText)%4
    if leftHorsemen != 0:
        fourHorsemen += 1
    
    #print "Character divided by 4: ", fourHorsemen
    #print "Remaining character: ", leftHorsemen
    
    if(leftHorsemen > 0):
        toAdd = 4-leftHorsemen    
        #print "So must add: ", toAdd
        for i in range(0, toAdd):
            binaryPlainText.append('00100000')
    
    #print "Size now: ", len(binaryPlainText)
    start = 0
    
    #binaryPlainText = map(int, binaryPlainText)
    #firstKey = map(int, firstKey)
    #secondKey = map(int, secondKey)
    
    XORedText = []
    for i in range(0, len(binaryPlainText)/4):
        for j in range(0, 4):
            #encryptedText.append(xor(int(binaryPlainText[start]), int(firstKey[j])))
            #print "Start: ", start
            #print "Binary Plain Text: ", binaryPlainText[start]
            #print "Key: ", firstKey[j]
            tempFir = int(binaryPlainText[start], 2)
            tempSec = int(firstKey[j], 2)
            tempXor = xor(tempFir,  tempSec)
            finalXor = '{0:08b}'.format(tempXor)
            #print "XOR: ", finalXor
            XORedText.append(finalXor)
            start = start + 1
    
    #print "Start now: ", start
    
    start = 0
    
    #print XORedText
    
    addModedText = []
    
    for i in range(0, len(binaryPlainText)/4):
        for j in range(0, 4):
            #addModedText.append(int(XORedText[start]) + int(secondKey[j]))
            tempFir = int(XORedText[start], 2)
            tempSec = int(secondKey[j], 2)
            res = tempFir + tempSec
            #print "res: ", res
            #print modulus64(res)
            res = modulus64(res)
            #print chr(res)
            #temp = repr(res)
            #print res
            res = '{0:08b}'.format(res)
            
            addModedText.append(res)
            start = start + 1
    
    #print "Start now: ", start
    
    #print addModedText
    
    
    
    return addModedText

def decrypt(binaryPlainText, binaryKey):
    
    firstKey = []
    secondKey = []
    
    for i in range(0, len(binaryKey)):
        if i <= 3:
            firstKey.append(binaryKey[i]);
        else:
            secondKey.append(binaryKey[i]);
                            
    #print "firstKey: ", firstKey
    #print "secondKey: ", secondKey
    
    start = 0
    
    dphaseone = []
    
    for i in range(0, len(binaryPlainText)/4):
        for j in range(0, 4):
            #addModedText.append(int(XORedText[start]) + int(secondKey[j]))
            res = modulus64(int(binaryPlainText[start], 2))
            tempFir = res
            tempSec = int(secondKey[j], 2)
            sul = tempFir - tempSec
            #print "res: ", res
            #print modulus64(res)
            
            #print chr(res)
            #temp = repr(res)
            #print res
            sul = '{0:08b}'.format(sul)
            
            dphaseone.append(sul)
            start = start + 1
    
    #print "Start now: ", start

    start = 0
    
    finalres = []
    
    for i in range(0, len(binaryPlainText)/4):
        for j in range(0, 4):
            #encryptedText.append(xor(int(binaryPlainText[start]), int(firstKey[j])))
            #print "Start: ", start
            #print "Binary Plain Text: ", binaryPlainText[start]
            #print "Key: ", firstKey[j]
            tempFir = int(dphaseone[start], 2)
            tempSec = int(firstKey[j], 2)
            tempXor = xor(tempFir,  tempSec)
            finalXor = '{0:08b}'.format(tempXor)
            #print "XOR: ", finalXor
            finalres.append(finalXor)
            start = start + 1
    
    #print "dphaseone: ", dphaseone
    #print "finalres: ", finalres
    return finalres

binaryAscii = []
finalBinaryAscii  = []    

#------------------------------------------------------------------------------

plainText = raw_input("Enter string to encrypt: ");
#print "String to encrypt is: ", plainText

key = 'Security'
print "Key is: ", key

keyASCII = [ord(c) for c in key]
#print "Key in ASCII: ", keyASCII

keyASCBin = [] #keyASCIIBinary

for i in keyASCII:
    keyASCBin.append("{0:b}".format(i))

#print "Key ASCII in Binary: ", keyASCBin

plainTextASCII = [ord(c) for c in plainText]
#print "Plain Text in ASCII: ", plainTextASCII

plainTextBinASC = [] #plainTextBinaryASCII

for i in plainTextASCII:
    plainTextBinASC.append("{0:b}".format(i))

#print "Plain Text ASCII in Binary: ", plainTextBinASC
    
finalPlTxBin = [] #finalPlainTextBinary

               
               
for i in plainTextBinASC:
    #print "Plain Text in Binary: ", i
    size = len(repr(int(i)))
    #print "Size is: ", size
    toEight = 8-size
    #print "Zero to add: ", toEight
    for num in range(0, toEight+1):
        temp = "0"+i
    #print "Result: ", temp
    finalPlTxBin.append(temp)    

#print "Final Plain Text to Encrypt: ", finalPlTxBin

finalKeyBin = []

for i in keyASCBin:
    #print "keyBinary: ", i
    size = len(repr(int(i)))
    #print "Size is: ", size
    toEight = 8-size
    #print "Zero to add: ", toEight
    for num in range(0, toEight+1):
        temp = "0"+i
    #print "Result: ", temp
    finalKeyBin.append(temp)    

#print "Final Key for Encryption: ", finalKeyBin

keyFirst = ['00100000', '00100100', '00101000', '00101100', '00110010', '00110110', '00111010', '00111100']
#32, 36, 40, 44, 50, 54, 58, 60

keySecond = ['01000111', '01001011', '01001111', '01010011', '01011011', '01011101', '01011111', '01100001']
#71, 75, 79, 83, 91, 93, 95, 97

encrypted = []
decryptedBack = []


encrypted = encrypt(finalPlTxBin, finalKeyBin)

#print "Encryption Result: ", encrypted

printer = []


for i in encrypted:
    temp = int(i, 2)
    temp2 = unichr(temp)
    printer.append(temp2)
    
finalPrinter = ''.join(printer)
print "Encryption Text: ", finalPrinter
    
decryptedBack = decrypt(encrypted, finalKeyBin)

#print "Decryption Result: ", decryptedBack

pprinter = []

for i in decryptedBack:
    temp = int(i, 2)
    temp2 = unichr(temp)
    pprinter.append(temp2)

finalPprinter = ''.join(pprinter)
print "Decryption Text: ", finalPprinter

temp = []


