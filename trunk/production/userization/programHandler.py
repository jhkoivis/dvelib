
import os
from setPathVariable import SetPathVariable

class ProgramHandler:

    def handleFlagged(self, dirName):
        flagDict = {'android'   : self.hasAndroid,
                    'python27'  : self.hasPython,
                    'python26'  : self.hasPython,
                    'python30'  : self.hasPython,
                    'python31'  : self.hasPython,
                    'cygwin'    : self.hasCygwin}
        compDir = os.path.basename(dirName).lower()
        for k,v in flagDict.iteritems():
            if compDir == k:
                v(dirName)
                
    def hasPython(self, dir):
        #print 'hasPython', dir
        spv = SetPathVariable()
        spv.winAppendPath(dir)
        pass
    
    def hasAndroid(self, dir):
        #print 'hasAndroid', dir
        spv = SetPathVariable()
        spv.winAppendPath(dir + '/android-sdk/platform-tools')
        pass
    
    def hasCygwin(self, dir):
        #print 'hasCygwin', dir
        spv = SetPathVariable()
        spv.winAppendPath(dir)
        pass