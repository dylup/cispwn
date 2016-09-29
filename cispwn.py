#!/usr/bin/python

import serial
import sys
import getopt

#ser = serial.Serial('/dev/ttyUSB0') # open serial port
#print (ser.name) # check which port was really used
#ser.close() # close

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hv")
	except getopt.GetoptError:
		print 'Usage: ./cispwn.py'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h' or '-help':
			print 'Usage: ./cispwn.py'
			sys.exit()
		if opt == '-v':
			print 'cispwn.py Version 0.1'
			sys.exit()
	print 'Yay!'

if __name__ == "__main__":
	main(sys.argv[1:])
		


