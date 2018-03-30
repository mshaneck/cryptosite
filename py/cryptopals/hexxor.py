#!/usr/bin/python

import cgi, os, binascii, base64, string, sys
sys.path.append('..')
from resources import *
print "Content-Type: text/html\r\n\r\n"

if (os.environ["REQUEST_METHOD"]=="POST"):
    form = cgi.FieldStorage()
    hexval1 = form["hexstring1"].value
    hexval2 = form["hexstring2"].value
    print hexxor(hexval1, hexval2)
else :
    print "Come on. Just use the interface...\n"
