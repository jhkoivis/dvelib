
import subprocess
import youtube_dl_pyInterface
import time
from threading import Thread

class myCommand:
    
    def __init__(self, text):
        self.printable = text

    def execute(self):
        for i in range(10):
            print self.printable
            
class ExecuteCommandLine:
    
    def __init__(self, cmdStr):
        self.cmdStr = cmdStr
    
    def execute(self):
         subprocess.call(self.cmdStr, shell = True)
     
class DownloadYoutubeVideo():
    '''
        Setup for youtube-video-downloader.
        
        Note! thread is not picklable, therefore 
        you must have a separate class for that.
    '''
    
    def __init__(self, videoURL, id = None, argArray = []):
        self.videoURL = videoURL
        if id == None: 
            self.id = time.time()
        else:
            self.id = id
        if argArray == []:
            self.argArray = []
            self.setDefaultArguments()
        else:
            self.argArray = argArray
            
    def setDefaultArguments(self):
        '''
            Use tested set of arguments.
        '''
        self.argArray = ['-w'] # do not overwrite
        self.argArray.append('--rate-limit=20k') # download limit
        self.argArray.append('-c') # continue 
        self.argArray.append('-f') # format 1
        self.argArray.append('18') # format 2: mp4 width = 360
        self.argArray.append('-o') # outputString 1
        self.argArray.append('%(title)s-%(id)s.%(ext)s') # outputString 2
        
    def execute(self):
        # TODO: redirect prints to logFile, not to stdout
        self.argArray.append(self.videoURL)
        vT = DownloadYoutubeVideoThread(self.argArray) 
        vT.start()
         
class DownloadYoutubeVideoThread(Thread):
    
    def __init__(self, argArray):
        Thread.__init__(self)
        self.argArray = argArray
    
    def run(self):
        youtube_dl_pyInterface.youtubeDL(self.argArray)
 
        
            
            