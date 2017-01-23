import socket
from datetime import datetime

from getpass import getpass

BUFF_SIZE = 4096
MFTP = 103

def create_mftp_sock ( host, port ):
	print ( "Creating MFTP object on server: " + host + ":" + port)

	username = raw_input("FTP username: ")
	password = getpass( "pass: " )

	return ( MFTP, host, port, username, password, None )

def do_mftp_stuff ( *args ):

	host = 	socket.gethostbyname(args[1])
	port = int ( args[2] )
	username = args[3]
	password = args[4]
	datetime_object = args[5]

	sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)
	
	sock.connect ( ( host, port ) )
	sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

	print ( "Connecting to " + host + ":" + str ( port ) + "...")
	responce = sock.recv ( BUFF_SIZE )

	sock.send ( str.encode ( "USER " + username + "\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )

	sock.send ( str.encode ( "PASS " + password + "\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )

	sock.send( str.encode ( "CWD Documents/stud/nt/poller/ftptest\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )

	sock.send( str.encode ( "PASV\r\n" ) )

	responce = sock.recv ( BUFF_SIZE )
	responce = responce.decode()
	responce = responce.split ( "(" )[1]
	responce = responce.split ( ")" )[0]
	host_parts = responce.split ( "," )
	ip = host_parts[0] + "." + host_parts[1] + "." + host_parts[2] + "." + host_parts[3]
	prt = int ( host_parts[4] ) * 256 + int ( host_parts[5] )


	ftp_sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)
	
	ftp_sock.connect ( ( ip, prt ) )
	ftp_sock.setsockopt ( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )	

	sock.send ( str.encode ( "LIST\r\n" ) )
	
	responce = ftp_sock.recv ( BUFF_SIZE )
	ftp_sock.close()
	
	responce = responce.decode()
	responce = responce[43:55]
	last_datetime_object = datetime.strptime("2016 " + responce, '%Y %b %d %H:%M')
	
	sock.recv ( BUFF_SIZE )

	print("Last modified at " + str( last_datetime_object ) )

	if datetime_object == None or datetime_object < last_datetime_object:
		print ( "FILE HAS CHANGES! DOWNLOADING" )

		sock.send( str.encode ( "PASV\r\n" ) )

		responce = sock.recv ( BUFF_SIZE )
		responce = responce.decode()
		
		responce = responce.split ( "(" )[1]
		responce = responce.split ( ")" )[0]
		host_parts = responce.split ( "," )
		ip = host_parts[0] + "." + host_parts[1] + "." + host_parts[2] + "." + host_parts[3]
		prt = int ( host_parts[4] ) * 256 + int ( host_parts[5] )


		ftp_sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM)

		ftp_sock.connect ( ( ip, prt ) )
		ftp_sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )	

		sock.send ( str.encode ( "RETR test.txt\r\n" ) )
		responce = ftp_sock.recv ( BUFF_SIZE )
		ftp_sock.close()
		sock.recv ( BUFF_SIZE )

		file = open("FTP.txt", "w")
		file.write(responce.decode())
		file.close()

		sock.send ( str.encode ( "QUIT\r\n" ) )
		sock.recv ( BUFF_SIZE )

		lst = list( args )
		lst[5] = last_datetime_object
		return tuple( lst )
	else:
		print ("Nothing new.")
		sock.send ( str.encode ( "QUIT\r\n" ) )
		sock.recv ( BUFF_SIZE )
		return None