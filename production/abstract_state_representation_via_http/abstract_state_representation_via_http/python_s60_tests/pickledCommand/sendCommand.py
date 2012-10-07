

import sys
sys.path.append('/Users/jko/Documents/workspace/abstract_state_representation_via_http/python_s60_tests/asyncore_server_and_client')
import mySocket
import pickle
import StringIO
import asyncore
from acceptedCommands import *
from reloadableCommands import *
from time import sleep

class CommandingClient(mySocket.MySocketClient):
    
    def __init__(self, *args, **kwargs):
        #asyncore.socket_map.clear()
        mySocket.MySocketClient.__init__(self, *args, **kwargs)
        self.commandString = ""
    
    def handle_write(self):
        self.printVerbose(2, 'handle_write')
        
        if not self.written:
            self.send(self.commandString)
            self.written = 1
        if self.recieved and self.written:
            self.close()
   
    def reloadCommands(self):
        c = ReplaceReloadable()
        self._packCommand(c)
        
    def _packCommand(self, command):
        outFile = StringIO.StringIO()
        pickledC = pickle.dump(command, outFile) # this packs C to outFile
        stringToSend = outFile.getvalue() # decoding to string
        self.commandString = stringToSend
        print stringToSend
    
    def sendCommand(self):
        asyncore.loop()
            
    def setAndPackCommand(self, command):
        self._packCommand(c)



#client = CommandingClient("127.0.0.1", 12346, verbose = 10)
client = CommandingClient("192.168.3.3", 12350, verbose = 0)
c = ReplaceReloadable()
client.setAndPackCommand(c)
client.sendCommand() 

client = CommandingClient("192.168.3.3", 12350, verbose = 0)
c = SimpleCommand()
client.setAndPackCommand(c)
client.sendCommand() 
#c = ExecuteCommandLine('ls -lha /home/jko')
#c = DownloadYoutubeVideo('http://www.youtube.com/view_play_list?p=8DDC5E42E0120693')

#client.reloadCommands()
#client.sendCommand()
#sleep(5)
#client.setAndPackCommand(c)
#client.sendCommand()   

