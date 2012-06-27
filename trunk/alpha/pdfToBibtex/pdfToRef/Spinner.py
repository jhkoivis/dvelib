import threading
import sys, os
import time
import unicodedata

class SpinCursor(threading.Thread):
    """ A console spin cursor class """
    
    def __init__(self, msg='',maxspin=0,minspin=10,speed=5):
        # Count of a spin
        self.count = 0
        self.out = sys.stdout
        self.flag = False
        self.max = maxspin
        self.State = "Failed"
        self.min = minspin
        # Any message to print first ?
        self.msg = msg
        # Complete printed string
        self.string = ''
        # Speed is given as number of spins a second
        # Use it to calculate spin wait time
        self.waittime = 1.0/float(speed*4)
        if os.name == 'posix':
            self.spinchars = (unicodedata.lookup('FIGURE DASH'),u'\\ ',u'| ',u'/ ')
        else:
            # The unicode dash character does not show
            # up properly in Windows console.
            self.spinchars = (u'-',u'\\ ',u'| ',u'/ ')        
        threading.Thread.__init__(self, None, None, "Spin Thread")
        
    def spin(self):
        """ Perform a single spin """

        for x in self.spinchars:
            self.string =  "...\t" + x + "\r" + self.msg
            self.out.write(self.string.encode('utf-8'))
            self.out.flush()
            time.sleep(self.waittime)
    def setMsg(self,msg):
        self.msg = msg
    def setState(self,state):
        self.State = state
    def run(self):

        while (not self.flag):#and ((self.count<self.min) or (self.count<self.max)):
            self.spin()
            self.count += 1
        # Clean up display...
        self.out.write(" "*6)
        self.out.write("["+self.State+"]\n")
        
        
    def stop(self):
        self.flag = True
        
def startSpin(text):
    spin = SpinCursor(msg=text)
    spin.start()
    return spin

def stopSpin(spin,text):
    spin.setState(text)
    spin.stop()
    spin.join()