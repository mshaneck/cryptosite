#!/usr/bin/python

import cgi, os, binascii, base64, string, sys, re
sys.path.append('..')
from resources import *

print "Content-Type: text/html\r\n\r\n"

if (os.environ["REQUEST_METHOD"]=="POST"):
    form = cgi.FieldStorage()

    form_file = form['ciphertext']
    ciphertext_lines = ""
    while True:
        chunk = form_file.file.read(100000)
        if not chunk:
            break
        ciphertext_lines += chunk
    # Is this hex encoded or base64 encoded?
    #print ciphertext_lines
    data=""
    hexPattern = re.compile("^[A-Fa-f0-9\n]+$")
    b64Pattern = re.compile("^[A-Za-z0-9/+=\n]+$")
    if (hexPattern.match(ciphertext_lines)):
        data = ciphertext_lines.decode('hex')
    elif (b64Pattern.match(ciphertext_lines)):
        data=base64.b64decode(ciphertext_lines)
    else:
        print "File format not recognized"
        exit()
    maxKeySize=42
    results=bestVigenereDecrypt(data, maxKeySize, False, False)
    print "Key: " + results[1] + "<br>\n"
    print "<pre>"+results[0]+"</pre><br>\n"

else :
    print "Come on. Just use the interface...\n"
