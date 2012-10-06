

import sys
sys.path.append('/Users/jko/Documents/workspace/abstract_state_representation_via_http/python_s60_tests/asyncore_server_and_client')
import mySocket
import pickle
import StringIO
import asyncore
from acceptedCommands import *

class CommandingClient(mySocket.MySocketClient):
    
    def __init__(self, *args, **kwargs):
        mySocket.MySocketClient.__init__(self, *args, **kwargs)
        self.commandString = ""
    
    def handle_write(self):
        self.printVerbose(2, 'handle_write')
        
        if not self.written:
            self.send(self.commandString)
            self.written = 1
        if self.recieved and self.written:
            self.close()
            
    def setAndPackCommand(self):
        #c = ExecuteCommandLine('ls /Users/jko -lha')
        c = DownloadYoutubeVideo('http://www.youtube.com/view_play_list?p=8DDC5E42E0120693')
        outFile = StringIO.StringIO()
        pickledC = pickle.dump(c, outFile) # this packs C to outFile
        stringToSend = outFile.getvalue() # decoding to string

        self.commandString = stringToSend


asyncore.socket_map.clear()
client = CommandingClient("127.0.0.1", 12349, verbose = 10)
client.setAndPackCommand()
asyncore.loop()    

