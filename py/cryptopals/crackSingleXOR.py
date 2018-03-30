#!/usr/bin/python

import cgi, os, binascii, base64, string, sys
sys.path.append('..')
from resources import *

print "Content-Type: text/html\r\n\r\n"

if (os.environ["REQUEST_METHOD"]=="POST"):
    form = cgi.FieldStorage()
    ciphertext = form["ciphertext"].value
    #print ciphertext
    key, score, plaintext = bestDecryption(ciphertext, False)
    print "Key: " + '{:02x}'.format(key)+"<br>\n"
    print "Plaintext: " + plaintext+"<br>\n"
else :
    print "Come on. Just use the interface...\n"
