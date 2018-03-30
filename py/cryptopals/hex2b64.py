#!/usr/bin/python

import cgi, os, binascii, base64, string
print "Content-Type: text/html\r\n\r\n"

if (os.environ["REQUEST_METHOD"]=="POST"):
    form = cgi.FieldStorage()
    hexval = form["hexstring"].value
    b64 = base64.b64encode(hexval.decode('hex'))
    print b64
else :
    print "Come on. Just use the interface...\n"
