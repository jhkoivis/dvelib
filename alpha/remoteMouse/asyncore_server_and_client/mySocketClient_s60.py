
import asyncore

class Verbose:
    
    def __init__(self, verbose = 0):
        self.verbose = verbose
    
    def printVerbose(self, verbose, text):
        if self.verbose >= verbose: 
            print "[%.4lf, verbose: %d] %s" % (time.time(),
                                               verbose,
                                               text)

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
            
            
            
            
            
            
b = MySocketClient("", 12377, verbose = 1)
asyncore.loop()
            
            
            