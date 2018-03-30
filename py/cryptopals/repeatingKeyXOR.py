#!/usr/bin/python

import cgi, os, binascii, base64, string, sys
sys.path.append('..')
from resources import *

print "Content-Type: text/html\r\n\r\n"

if (os.environ["REQUEST_METHOD"]=="POST"):
    form = cgi.FieldStorage()
    plaintext = form["plaintext"].value #This is in ASCII
    key = form["key"].value
    print repeatingXORCrypt(plaintext, key)
else :
    print "Come on. Just use the interface...\n"
