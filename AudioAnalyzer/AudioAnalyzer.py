
import wave
import os

class AudioAnalyzer:
    
    def __init__(self):
        """
        TODO
        """
        self.externalEncoder = "/opt/local/bin/ffmpeg -y -i infile outfile 2> /dev/null"
        
    def convertToWavWithExternal(self,infile,outfile):
        """
        converts file to wav using external tools.
        returns exit code for command
        """
        command = self.externalEncoder.replace("infile", infile).replace("outfile", outfile)
        return os.system(command)
        
        
    def loadAudioFile(self, filename):
        """
        returns fileHandle or error
        """
        file = wave.open(filename,'r')
        return file
    
    def getAudioAsArray(self,file):
        """
        returns audio file as array of floats
        """
        a = 2
        