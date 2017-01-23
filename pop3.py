import socket
from datetime import datetime
from getpass import getpass

BUFF_SIZE = 4096
POP3 = 100

def create_pop3_sock ( host, port ):
	print ( "Creating POP3 object on server: " + host + ":" + port)

	username = raw_input("POP3 username: ")
	password = getpass("pass: ")

	return ( POP3, host, port, username, password, None )

def do_pop3_stuff ( *args ):
	
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
	
	sock.send ( str.encode ( "USER " + username + "\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )

	sock.send ( str.encode ( "PASS " + password + "\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )

	sock.send( str.encode ( "STAT\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )
	responce = responce.decode()
	last = responce.split(" ")[1]
	print( "Total " + last + " e-mail(s)." )

	print ( "Checking last e-mail...")
	sock.send(str.encode("TOP " + last + " 0\r\n"))
	responce = "".encode()

	while ".\r\n" not in responce.decode():
		responce += sock.recv(BUFF_SIZE)

	responce = responce.decode()
	responce = responce.split ( "\nDate: " )[1]
	responce = responce.split ( "\r" )[0]
	responce = responce.split ( ", " )[1]

	last_datetime_object = datetime.strptime(responce, '%d %b %Y %H:%M:%S %z')
	print("Last e-mail received at " + str( last_datetime_object ) )

	if datetime_object == None or datetime_object < last_datetime_object:
		print ( "NEW E-MAIL AVAILABLE!" )

		lst = list( args )
		lst[5] = last_datetime_object
		return tuple( lst )
	else:
		print ("Nothing new.")
		return None