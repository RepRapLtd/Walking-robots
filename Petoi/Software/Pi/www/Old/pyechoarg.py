#!/usr/bin/python3

import sys
#import cgi, cgitb 
#cgitb.enable() 

#data = cgi.FieldStorage()

data = " ".join(sys.argv[1:])

print("Content-Type: text/html")
print(data)

