from fractions import gcd
from Crypto.Cipher import AES

def hexxor(hexval1, hexval2):
    hexxor = int(hexval1, 16) ^ int(hexval2, 16)
    return "{0:0{1}x}".format(hexxor, len(hexval1))

def xorEncrypt(plaintextASCII, key):
    return ''.join([ chr(ord(a) ^ ord(key)) for (a) in plaintextASCII])

def bestDecryption(ciphertext, justASCII):
    ciphertextlen = len(ciphertext)/2
    #print ciphertextlen
    bestKey=-1
    maxScore=-1
    bestPlaintext=""
    validRange = range(256)
    if (justASCII):
        validRange = range(32,127)
    for i in validRange:
        if justASCII:
            plaintext = asciiDecrypt(ciphertext, chr(i))
        else:
            plaintext = xorDecrypt(ciphertext, ciphertextlen, i).decode('hex')
        score=englishScore(plaintext)
        #print score, plaintext
        if score > maxScore:
            maxScore=score
            bestKey=i
            bestPlaintext = plaintext
    #print bestKey, maxScore
    #print bestPlaintext
    return (bestKey, maxScore, bestPlaintext)

def asciiDecrypt(ciphertext, k):
    decrypted=""
    for c in ciphertext:
        decrypted += chr(((ord(c.lower())-97) - (ord(k.lower())-97))%26)
    return decrypted

def xorDecrypt(ciphertext, ciphertextlen, key):
    key="{0:0{1}x}".format(key,2)
    key=key*ciphertextlen
    hexplain=hexxor(ciphertext, key)
    return hexplain

def englishScore(hexStr):
    #First ensure that all characters are printable
    #if all(c in string.printable for c in hexStr):
        # compute count of alphabet characters over total string length
        # rudimentary but seems to work for this example...
        letterCount=0
        for c in hexStr:
            if c.isalpha() or c==" " or c=="'" or c=="." or c=="," or c=="?" or c=="!":
                letterCount=letterCount+2
            if c.upper() in "ETAOIN SHRDLU":
                letterCount=letterCount+3
            #if c in "LXCF0123456789{_}": #The last bit is for AlexCTF2017
                #letterCount = letterCount+3
        #print letterCount, len(hexStr)
        baseScore = float(letterCount)/len(hexStr)
        #words=hexStr.split(" ")
        # somehow incorporate the word count into the score
        #baseScore = baseScore + float(len(words))/len(hexStr)
        return baseScore
    #else:
        #return 0.0

def detectXORDecryption(ciphertext_lines):
    i=1
    maxScore=0
    bestPlaintext=""
    bestLine=-1
    for line in ciphertext_lines.splitlines():
        key, score, plaintext=bestDecryption(line.rstrip(), False)
        if (score>maxScore):
            maxScore=score
            bestPlaintext=plaintext
            bestKey=key
            bestLine=i
        i=i+1
    return (bestLine, bestPlaintext, bestKey)

def repeatingXORCrypt(plain, key):
    #First make the key the same length as the plaintext
    hexPlain=plain.encode('hex')
    xorkey = key.encode('hex')
    xorkey = xorkey*len(hexPlain)
    xorkey = xorkey[0:len(hexPlain)]
    #Then hexxor
    return hexxor(hexPlain, xorkey)

def hammingDistance(string1, string2):
    assert len(string1)==len(string2)
    distance=0
    for i,c in enumerate(string1):
        x = ord(c)^ord(string2[i:i+1])
        while (x):
            x = x&(x-1)
            distance=distance+1
    return distance

def getNAvgHammingDistances(data, maxKeyLength):
    avgHDs = []
    datalen=len(data)

    for keysize in range(2, maxKeyLength):
        #Take as many hamming distances as possible
        hd=0
        for i in range(0, datalen/(keysize*2)):
            str1 = data[keysize*2*i:keysize*(2*i+1)]
            str2 = data[keysize*(2*i+1):keysize*(2*i+2)]
            hd = hd+hammingDistance(str1, str2)
        #average hamming distance between substrings
        #print hd, datalen, keysize, float(datalen/(keysize*2))
        hd = float(hd)/float(datalen/(keysize*2))
        #normalize it based on keysize
        hd = hd/float(keysize)
        avgHDs.append([hd, keysize])

        #str1=data[0:keysize]
        #str2=data[keysize:2*keysize]
        #str3=data[2*keysize:3*keysize]
        #str4=data[3*keysize:4*keysize]
        #hd1 = hammingDistance(str1, str2)
        #hd2 = hammingDistance(str3, str4)
        #hd = (float(hd1+hd2)/2.0)/float(keysize)
        #avgHDs.append([hd, keysize])
    avgHDs.sort()
#    print avgHDs
    #exit(1)
    return avgHDs


def bestVigenereDecrypt(data, maxKeySize, exactKeySize, justASCII):
    if (not exactKeySize):
        hds = getNAvgHammingDistances(data, maxKeySize)
        #print "Best keysize and distance: ", hds[0][1], hds[0][0]
        #print "Second best keysize and distance: ", hds[1][1], hds[1][0]
        #split the data into chunks of size bestKeySize

        # Algorithm idea from https://trustedsignal.blogspot.com/2015/06/xord-play-normalized-hamming-distance.html
        gcd12=gcd(hds[0][1], hds[1][1])
        gcd13=gcd(hds[0][1], hds[2][1])
        gcd23=gcd(hds[1][1], hds[2][1])
        bestKeySize=-1
        #if (gcd12 != 1):
            # This next one could possibly be improved to search a configurable top n
            #    if (gcd12 == hds[0][1] or gcd12 == hds[1][1] or gcd12 == hds[2][1] or gcd12 == hds[3][1]):
            #        if (gcd12==gcd13 and gcd12==gcd23) or (gcd12 == hds[0][1] or gcd12==[1][1]):
            #            bestKeySize=gcd12
        if (bestKeySize == -1):
            bestKeySize=hds[0][1]
    else:
        bestKeySize = maxKeySize

    #print bestKeySize
    lines=[data[i:i+bestKeySize] for i in range(0, len(data), bestKeySize)]
    rearrangedLines=""

    for i in range(0,bestKeySize):
        for line in lines:
            try:
                rearrangedLines+=line[i]
            except IndexError:
                continue

    vigenereLines=[rearrangedLines[i:i+len(lines)] for i in range(0,len(data), len(lines))]
    #print vigenereLines
    i=0
    vigenereKeys=""
    #print vigenereLines

    for line in vigenereLines:
        #print '--------------------------'
        #print len(line)
        #print line.encode('hex')
        if justASCII:
            vigenereKey, vigenereScore, vigenerePlaintext=bestDecryption(line, justASCII)
        else:
            vigenereKey, vigenereScore, vigenerePlaintext=bestDecryption(line.encode('hex'), justASCII)
        #print vigenereKey, vigenereScore
        vigenereKeys+="{0:0{1}x}".format(vigenereKey,2)
    maybePlain = repeatingXORCrypt(data, vigenereKeys.decode('hex')).decode('hex')
    #print maybePlain
    score =englishScore(maybePlain)
    #print score
    return [maybePlain, vigenereKeys.decode('hex')]
