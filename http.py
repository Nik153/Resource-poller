import socket
from datetime import datetime

BUFF_SIZE = 4096
HTTP = 102

def create_http_sock ( host, port ):
	print ( "Creating HTTP object on server: " + host + ":" + port )

	return ( HTTP, host, port, None )

def do_http_stuff ( *args ):
	host = socket.gethostbyname ( args[1] )
	port = int ( args[2] )

	datetime_object = args[3]

	sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

	sock.connect ( ( host, port ) )
	sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

	print ( "Connecting to " + host + ":" + str ( port ) + "...")

	page = raw_input("Page (ex '/index' ): ")

	sock.send ( str.encode ( "HEAD " + page + " HTTP/1.0\r\n\r\n" ) )
	responce = sock.recv ( BUFF_SIZE )
	responce = responce.decode()	
	responce = responce.split ( "Last-Modified: " )[1]
	responce = responce.split ( "\n" )[0]

	last_datetime_object = datetime.strptime(responce[6:-5], '%d %b %Y %H:%M:%S')
	print ( "Last update at " + str ( last_datetime_object ) )

	sock.close();

	if datetime_object == None or datetime_object < last_datetime_object:

		sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )

		sock.connect ( ( host, port ) )
		sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

		print ( "Downloading page" )
		sock.send ( str.encode ( "GET " + page + " HTTP/1.0\r\n\r\n" ) )

		responce = "".encode()
		while "</html>" not in responce.decode():
			responce += sock.recv ( BUFF_SIZE )	
		sock.close()

		file = open("HTTP.txt", "w")
		file.write(responce.decode())
		file.close()

		lst = list( args )
		lst[3] = last_datetime_object
		return tuple( lst )
	else:
		print("Nothing new.")
		return None
