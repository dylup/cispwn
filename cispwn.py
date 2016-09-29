#!/usr/bin/python

import serial
import sys
import getopt

version = 'Version 0.1'

#ser = serial.Serial('/dev/ttyUSB0') # open serial port
#print (ser.name) # check which port was really used
#ser.close() # close
#test
def rommon(console):
	rom=false
	while rom==false:
		prompt=read_serial(console)
		if "Press RETURN" in prompt:
			print "Power cycle the router again"
			time.sleep(5)
		else if "Self decompressing the image" in prompt:
			send_command(console,'\x03')
			rom=true
			print "rommon is ready"
			send_command(console,'confreg 2042')
			send_command(console,'boot')
			print "Booting"

def copy_config(console):
	#tftp the config file

def decrypt_passwords(console):
	#copy_config() and parse the file for cisco 7 passwords, then crack them and display them in plaintext

def randomize_passwords(console):
	#copy_config() parse the file for passwords, replace them with random encrypted passwords

def delete_config(console):
	#delete the startup config file

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
		opts, args = getopt.getopt(argv, "hV", ['help',
												'version'])
	except getopt.GetoptError:
		print 'Usage: ./cispwn.py <args>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print 'Usage: ./cispwn.py\n'
			print 'Arguments:'
			print '\t-V or --version\t\tShow version info'
			print '\t-h or --help\t\tShow this screen'
			sys.exit()
		if opt in ('-V', '--version'):
			print 'cispwn.py ' + version
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
	


