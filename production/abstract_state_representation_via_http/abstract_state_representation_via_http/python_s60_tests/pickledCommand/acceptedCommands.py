
import subprocess
import youtube_dl_pyInterface
import time
from threading import Thread
import reloadableCommands

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
        
class ReplaceReloadable:
    """
    Replaces reloadableCommands class and loads it to memory.
    """
    
    def __init__(self):
        self.classString = []
        self.loadLocalToMemory()

    def _getReloadableCommandsFileName(self, inputFn = 'reloadableCommands.py'):
        import inspect, os
        thisDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        reloadableCommandsFn = thisDir + '/' + inputFn
        return reloadableCommandsFn

    def loadLocalToMemory(self):
        """
        Loads local string to memory
        """
        textArray = open(self._getReloadableCommandsFileName(), 'r').readlines()
        self.classString = textArray
        
    def backupExisting(self, inputFn = 'reloadableCommands.py'):
        """
        Move previous file to safety with time stamp.
        """
        import shutil
        source = self._getReloadableCommandsFileName()
        target = source + '.%f' % (time.time())
        shutil.copy(source, target)
        
    def writeNewReloadableCommands(self):
        target = self._getReloadableCommandsFileName()
        outFile = open(target, 'w')
        for line in self.classString:
            outFile.write(line)
        outFile.close()

 # reload has to be in ExecutingServer object i.e. the 
 # object which is executing has to reload the module 
 #   def reloadReloadableCommands(self):
 #       reload(reloadableCommands)
        
    def execute(self):
        self.backupExisting()
        self.writeNewReloadableCommands()
 
        
            
            