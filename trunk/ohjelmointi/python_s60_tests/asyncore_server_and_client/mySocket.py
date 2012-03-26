

'''
    This file contains five classes. 
    
    Verbose:
        just for errorlogs, everyone inherits this.
    
    MyService:
        Thread wrapper for MySocketServer.
        
    MyClient:
        Thread wrapper for MySocketClient.
        
    MyChannel:
        Channel for the MySocketServer.
        You can keep the server alive and just close the channel
        
    MySocketServer:
        Bind to address and listen.
        
    MySocketClient:
        Write and read to address and quit.
        
    
    Modify MySocketClient.handle_read (and write) and 
    MyChannel.handle_read (and write) to get the functionality you want.


    TODO: implement readable(), writeable(), see: http://docs.python.org/library/asyncore.html

'''


import time
import socket
import asyncore
from threading import Thread
import sys

class Verbose:
    
    def __init__(self, verbose = 0):
        self.verbose = verbose
    
    def printVerbose(self, verbose, text):
        if self.verbose >= verbose: 
            print "[%.4lf, verbose: %d] %s" % (time.time(),
                                               verbose,
                                               text)

class MyService(Thread, Verbose):
    
    def __init__(self, port, verbose = 1):
        Verbose.__init__(self, verbose)
        Thread.__init__(self)
        self.port = port
        self.server = None
        self.verbose = verbose
        
    def run(self):
        self.printVerbose(1,'Server started')
        asyncore.socket_map.clear()
        self.server = MySocketServer(self.port)
        asyncore.loop(timeout=2)
        self.printVerbose(1, 'Server stopped')
        
    def quit(self):
        #asyncore.socket_map.clear()
        sys.exit()

class MyClient(Thread, Verbose):
    
    def __init__(self, host, port, verbose = 1):
        Verbose.__init__(self, verbose = verbose)
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.verbose = verbose
        
    def run(self):
        self.printVerbose(1,'Client started')
        asyncore.socket_map.clear()
        self.client = MySocketClient(self.host, self.port, verbose = self.verbose)
        asyncore.loop()
        self.printVerbose(1, 'Client stopped')
        
    def quit(self):
        #asyncore.socket_map.clear()
        sys.exit()

class MyChannel(asyncore.dispatcher, Verbose):

    def __init__(self, channel, verbose = 1, text = None):
        Verbose.__init__(self, verbose = verbose)
        asyncore.dispatcher.__init__(self, channel)
        self.text = text
        self.recieved = 0
        self.written = 0

    def handle_write(self):
        self.printVerbose(2, 'Handle Write')
        if not self.written:
            self.send('Hi from server!')
            self.written = 1
        # Do not close after write: client writes first and then reads.
        
    def handle_read(self):
        self.printVerbose(2, 'Handle Read')
        s = self.recv(20)
        if not self.recieved:
            print s
            self.recieved = 1
        if self.written:
            self.close()
       
    def handle_close(self):
        self.close()

class MySocketServer(asyncore.dispatcher, Verbose):
    
    def __init__(self, port, verbose = 1):
        Verbose.__init__(self, verbose)
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", self.port))
        self.listen(5)
        
    def handle_accept(self):
        self.printVerbose(2,'Connection Accept')
        channel, addr = self.accept()
        MyChannel(channel, verbose = self.verbose, text = 'Hi from server')
 
    def handle_close(self):
        self.printVerbose(2,'Connection Close')
        self.close()
        
class MySocketClient(asyncore.dispatcher,Verbose):
    
    def __init__(self, host, port, verbose = 1):
        Verbose.__init__(self, verbose)
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host,port))
        self.recieved = 0   # successful read
        self.written = 0    #  successful write
        
    def handle_connect(self):
        self.printVerbose(2, 'handle_connect')
        pass
    
    def handle_read(self):
        self.printVerbose(2, 'handle_read')
        s = self.recv(20)
        if not self.recieved:
            print s
            self.recieved = 1
        if self.written:
            self.close()

    def handle_close(self):
        self.printVerbose(2, 'handle_close')
        self.close()
    
    def handle_write(self):
        self.printVerbose(2, 'handle_write')
        if not self.written:
            self.send('Hi from client!')
            self.written = 1
        # Do not close after write: client writes first and then reads.
            
    