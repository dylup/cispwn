#!/usr/bin/python

import serial
import sys
import getopt

#ser = serial.Serial('/dev/ttyUSB0') # open serial port
#print (ser.name) # check which port was really used
#ser.close() # close
def rommon(console):
	rom=false
	while rom==false:
		prompt=read_serial(console)
		if "Press RETURN" in prompt:
			print "Power cycle the router again"
			time.sleep(5)
		if "Self decompressing the image" in prompt:
			send_command(console,'\x03')
			rom=true
			print "rommon is ready"



def read_serial(console):
	data_bytes=console.inWaiting()
	if data_bytes:
		return console.read(data_bytes)
	else:
		return ""

def send_command(console,cmd=''):
	console.write(cmd+'\r\n')
	time.sleep(1)
	return read_serial(console)

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hi:o")
	except getopt.GetoptError:
		print 'Usage: ./cispwn.py'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: ./cispwn.py'
			sys.exit()
	print 'Yay!'
	#console=serial.Serial(
		#	port='COM1',
		#	baudrate=9600,
		#	parity="N"
		#	stopbit=1,
		#	bytesize=8
		#	timeout=READ_TIMEOUT
		#)
	#if not console.isOpen():
		#print 'Error, a connection could not be made'
		#sys.exit()
	#Function for entering rommon goes here

if __name__ == "__main__":
	main(sys.argv[1:])
	


