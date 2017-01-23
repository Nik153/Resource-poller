import ssl
import socket
import signal
import getpass
import subprocess
import shutil
from time import sleep
from datetime import datetime

import pop3
import imap
import http
import mftp

BUFF_SIZE = 4096
DELAY = 5

POP3 = 100
IMAP = 101
HTTP = 102
MFTP = 103

servers = []

def exit_handler ( arg1, arg2 ):
    print()
    print("Good Bye!")
    exit(0)

if __name__ == "__main__":
	
	signal.signal(signal.SIGINT, exit_handler)
	
	subprocess.call ( "clear", shell = True )
	columns = shutil.get_terminal_size().columns
	
	def write_big_mess ( mess ):
		l = len( mess )
		left = int ( l / 2 ) 
		right = l - left

		print ( ( "*" * columns ) )
		print ( ( "*" * 5 + int( columns / 2 - 5 - left ) * " " + mess + int( columns / 2 - 5 - right ) * " " + 5 * "*" ) )	
		print ( ( "*" * columns ) )
		
	write_big_mess ( "WELCOME TO POLLER" )

# POP3 server
	host = raw_input("POP3 server: ")
	port = raw_input("POP3 port: ")
	servers.append ( pop3.create_pop3_sock ( host, port ) )
	print()

# IMAP server
	host = raw_input("IMAP server: ")
	port = raw_input("IMAP port: ")
	servers.append ( imap.create_imap_sock ( host, port ) )
	print()

# HTTP server
	host = raw_input("HTTP server: ")
	port = raw_input("HTTP port: ")
	servers.append ( http.create_http_sock ( host, port ) )
	print()

# FTP server
	host = raw_input("FTP server: ")
	port = raw_input("FTP port: ")
	servers.append ( mftp.create_mftp_sock ( host, port ) )
	print()
	
	while True:
		for server in servers:
			try:
				if server[0] == POP3:
					write_big_mess( "POP3 WORKING")
					result = pop3.do_pop3_stuff ( *server )
		
				elif server[0] == IMAP:
					write_big_mess( "IMAP WORKING" )
					result = imap.do_imap_stuff( *server )

				elif server[0] == HTTP:
					write_big_mess( "HTTP WORKING" )
					result = http.do_http_stuff( *server )

				elif server[0] == MFTP:
					write_big_mess( " FTP WORKING" )
					result = mftp.do_mftp_stuff( *server )

				if result != None:
					servers [ servers.index ( server ) ] = result

			except:
					print ( "Unexpected error. Deleting server from list.")
					servers.remove ( server )



		write_big_mess( "SLEEPING")
		for i in range(0, DELAY):
			print( DELAY - i )
			sleep(1)
		
		subprocess.call ( "clear", shell = True )
		write_big_mess("POLLER")

	print("DONE")
