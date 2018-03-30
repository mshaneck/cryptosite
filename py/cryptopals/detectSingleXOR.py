#!/usr/bin/python

import cgi, os, binascii, base64, string, sys
sys.path.append('..')
from resources import *

print "Content-Type: text/html\r\n\r\n"

if (os.environ["REQUEST_METHOD"]=="POST"):
    form = cgi.FieldStorage()

    form_file = form['ciphertexts']
    ciphertext_lines = ""
    while True:
        chunk = form_file.file.read(100000)
        if not chunk:
            break
        ciphertext_lines += chunk
    #for c in ciphertext_lines:
    #    print c+"<br>\n"
    #print ciphertext_lines
    bestLine, bestPlaintext, bestKey = detectXORDecryption(ciphertext_lines)

    print "Plaintext number: " + str(bestLine) + "\n<br>"
    print bestPlaintext + " (" + hex(bestKey) + ")\n"
else :
    print "Come on. Just use the interface...\n"
