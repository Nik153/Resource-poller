import socket
from datetime import datetime
from getpass import getpass

BUFF_SIZE = 4096
IMAP = 101

def create_imap_sock ( host, port ):
	print ( "Creating IMAP object on server: " + host + ":" + port )

	username = raw_input("IMAP username: ")
	password = getpass("pass: ")

	return ( IMAP, host, port, username, password, None )

def do_imap_stuff ( *args ):
	
	host = 	socket.gethostbyname(args[1])
	port = int ( args[2] )
	username = args[3]
	password = args[4]
	datetime_object = args[5]

	sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)
#	sock = ssl.wrap_socket ( sock )

	sock.connect ( ( host, port ) )
	sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

	print ( "Connecting to " + host + ":" + str ( port ) + "...")
	responce = sock.recv ( BUFF_SIZE )

	sock.send ( str.encode ( "A1 LOGIN " + username + " " + password + "\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )

	sock.send( str.encode ( "A2 SELECT INBOX\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )
	responce = responce.decode()
	responce = responce.split(" EXISTS")[0]
	last = responce.split(" ")[-1]
	print( "Total " + last + " e-mail(s)." )

	sock.send( str.encode ( "A3 FETCH " + last + " RFC822.HEADER\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )
	responce = responce.decode()
	responce = responce.split("Received: by")[1]
	responce = responce.split("\n")[1]
	responce = responce[-33:-7]

	print(responce)
	last_datetime_object = datetime.strptime(responce, '%d %b %Y %H:%M:%S %z')
	print("Last e-mail received at " + str( last_datetime_object ) )

	if datetime_object == None or datetime_object < last_datetime_object:
		print ( "NEW E-MAIL AVAILABLE!" )

		lst = list( args )
		lst[5] = last_datetime_object
		return tuple ( lst )
	else:
		print ( "Nothing new.")
		return None