import SocketServer
import select
import socket 

class Client:
	
	def __init__(self, target, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.target = target
		self.port = port 
		
	def connect(self):
		self.socket.connect((self.target, self.port))
	
class ForwarderServer(SocketServer.TCPServer):	
	
	def __init__(self, HP, handler, client):
		super(ForwarderServer, self).__init__(HP, ForwarderHandler)
		self.client = client

class ForwarderHandler(SocketServer.BaseRequestHandler):
	
	def setUp(self):
		self.server.client.connect()	
		
	def handle(self):
		while True:
			fdlist = [self.client.socket, self.request]
			(read, write, xlist) = select.select(fdlist, [], fdlist)
			for s in read: 
				if s.fileno() != self.client.socket.fileno():
					msg = s.recv(1024)
					print "S: " + repr(msg)
					if not msg: 
						break
					self.client.socket.send(msg)
				else:
					msg = s.recv(1024)
					print "S: " + repr(msg)
					if not msg: 
						break
					self.request.send(s.recv(1024))
		print "Server exit"
		
if __name__ == "__main__":
	HP = ("localhost", 9999)
	client = Client('freechess.org',23)
	server = (HP, ForwarderServer(HP, ForwarderHandler, client)
	server.serve_forever()