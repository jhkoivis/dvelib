
#####################################
# Executing server
#####################################
#
# maximum command length in chars (including pickle overhead)
maxPickledStringLength = 2048
# port to listen
port = 12350
#
#
#
#####################################
import sys
#sys.path.append('/Users/jko/Documents/workspace/abstract_state_representation_via_http/python_s60_tests/asyncore_server_and_client')
import mySocket
import pickle
import StringIO
import asyncore
from acceptedCommands import *
from reloadableCommands import *

class ExecutingChannel(mySocket.MyChannel):
    
    def __init__(self, *args, **kwargs):
        mySocket.MyChannel.__init__(self, *args, **kwargs)
    
    def handle_read(self):
        self.printVerbose(2, 'Handle Read') 
        stringToReceive = self.recv(maxPickledStringLength)
        if not self.recieved:
            self.unpackAndExecute(stringToReceive)
            self.recieved = 1
        if self.written:
            self.close()
    
    def unpackAndExecute(self, stringToReceive):
        reload(reloadableCommands)
        #print stringToReceive
        #reload(SimpleCommand)
        inFile = StringIO.StringIO()
        inFile.write(stringToReceive)
        inFile.seek(0, 0)
        receivedC = pickle.load(inFile)     
        receivedC.execute()
        

class ExecutingServer(mySocket.MySocketServer):
    
    def __init__(self, *args, **kwargs):
        mySocket.MySocketServer.__init__(self, *args, **kwargs)
    
    def handle_accept(self):
        self.printVerbose(2,'Connection Accept')
        channel, addr = self.accept()
        ExecutingChannel(channel, verbose = self.verbose, text = 'executing')

asyncore.socket_map.clear()
server = ExecutingServer(port, verbose = 10)
asyncore.loop(timeout=5)


## create package
#c = myCommand()
#outFile = StringIO.StringIO()
#pickledC = pickle.dump(c, outFile) # this packs C to outFile
#stringToSend = outFile.getvalue() # decoding to string
#
##############
## send string here ...
#stringToReceive = stringToSend
###############
#
## unpack package
#inFile = StringIO.StringIO()
#inFile.write(stringToReceive)
#inFile.seek(0, 0)
#
#receivedC = pickle.load(inFile)
#
#
## execute
#receivedC.execute()