
import Image
import pylab
import numpy

class CncFeedback:
    
    def __init__(self):
        self.pos = (0,0)
        self.velocity = (0,0)
        self.time = 0
        
        self.accuracy = 2
        
    def getDist(self, p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return numpy.sqrt(dx**2 + dy **3)

    def getTime(self):
        return self.time

    def getCurrentPos(self):
        return self.pos
    
    def setCurrentVelocity(self):
        return self.velocity
    
    def getCurrentVelocity(self):
        return self.velocity    

    def moveToStart(self, part):
        
        self.bladeUp()
        
        cp = self.getCurrentPos()
        tp = (part[0,0], part[0,1])
        t = self.getTime()
        while self.getDist(cp, tp) < 2:
             pass
        

    def bladeUp(self):
        pass
    
    def cut(self,part):
        pass
    
    def bladeDown(self):
        pass
        

class Blueprint:
    
    def __init__(self):
        pass
    
    def loadImage(self, fn):
        self.image = pylab.imread(fn)
        
    def imageToBinary(self):
        imax = numpy.max(self.image[:,:,0])
        imin = numpy.min(self.image[:,:,0])
        self.binaryImage = numpy.zeros(self.image[:,:,0].shape)
        self.binaryImage[self.image[:,:,0]==imax] = 1 
    
    def binaryToVectors(self):
        vectorList = []
        for i in range(1,self.binaryImage.shape[0] -1):
            for j in range(1, self.binaryImage.shape[1] -1):
                summa = numpy.sum(self.binaryImage[(i-1):(i+1), (j-1):(j+1)])
                if summa == 3 or summa == 2:
                    vectorList.append([j,i])
        self.vectorList = numpy.array(vectorList)
        
        self.vectorList2 = []
        cp = [self.vectorList[0,0],self.vectorList[0,1]]
        self.vectorList2.append(cp)
        self.vectorList[0,0] = -10000
        for i in range(1, self.vectorList.shape[0]):
            dx = self.vectorList[:,0] - cp[0]
            dy = self.vectorList[:,1] - cp[1]
            dist = dx**2 + dy**2
            
            try:
                minInd = numpy.argmin(dist)[0]
            except:
                minInd = numpy.argmin(dist)
            
            
            cp = [self.vectorList[minInd,0], self.vectorList[minInd,1]]
            #print minInd, dist[minInd], cp
            self.vectorList2.append(cp)
            self.vectorList[minInd,0] = -10000
        self.vectorList2 = numpy.array(self.vectorList2)
        
    def showImage(self):
        pylab.subplot(2,2,1)
        pylab.imshow(self.image)
        pylab.subplot(2,2,2)
        pylab.imshow(self.binaryImage)
        pylab.colorbar()
        pylab.subplot(2,2,3)
        pylab.plot(self.vectorList2[:,0], self.vectorList2[:,1])
        pylab.gca().invert_yaxis()
    
class Vectors:
    
    def __init__(self):
        pass
    
    def setPoints(self, pointArray):
        self.initialVectors = pointArray

    def divideIntoPieces(self):
        
        self.parts = []
        part = []
        part.append([self.initialVectors[0,0],
                     self.initialVectors[0,1]])
        for i in range(1,self.initialVectors.shape[0]):
            pp = part[-1]
            cp = self.initialVectors[i,:]
            if (pp[0] - cp[0])**2 + (pp[1] - cp[1])**2 > 2:
                self.parts.append(numpy.array(part))
                part = []
                part.append([self.initialVectors[i,0],
                             self.initialVectors[i,1]])
                print "break", i
            else:
                part.append([self.initialVectors[i,0],
                             self.initialVectors[i,1]])
        self.parts.append(numpy.array(part))
            
    def plotParts(self):
        print len(self.parts)
        pylab.subplot(2,2,4)
        #pylab.figure()
        for part in self.parts:
            print len(part)
            pylab.plot(part[:,0], part[:,1])#, 'k-', linewidth = 5)
        pylab.gca().invert_yaxis()
        pylab.gca().set_aspect(1)
        
    def ra(self, x, lag = 3):
        cs = numpy.cumsum(x)
        ra = (cs[lag:] - cs[:-lag])/lag 
        return ra
    
    def smooth(self):
        lag = 1
        for i in range(len(self.parts)):
            if self.parts[i].shape[0] <= lag: continue
            
            print self.parts[i].shape
            
            x = self.ra(self.parts[i][:,0], lag = lag)
            y = self.ra(self.parts[i][:,1], lag = lag)
            
            self.parts[i] = numpy.array([x,y]).T
            
            print self.parts[i].shape
        
        
        
        
        
        
        
