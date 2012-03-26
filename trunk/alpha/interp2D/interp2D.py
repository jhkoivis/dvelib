
import scipy.interpolate as si
import numpy

class Interp2D:
    
    def __init__(self, matrix = None):
        
        self.xMatrix = None
        self.yMatrix = None
        self.zMatrix = None
        
        if not matrix == None:
            self.setSpatial(matrix)

    
    def setSpatial(self, matrix):
        """
            Assumes cartesian coordinate system for matrix:
            first argument is X
            second argument is Y
            
            Notice that meshgrid assumes ij-coordinate system 
            (colums first, rows second). Hence reverse order
            of self.yMatrix, self.xMatrix
        
        """
        xVect = numpy.arange(matrix.shape[0])
        yVect = numpy.arange(matrix.shape[1])
        self.yMatrix, self.xMatrix = numpy.meshgrid(xVect, yVect) 
        self.zMatrix = matrix
        
    
    def simple(self, x, y, matrix = None):
        if self.xMatrix == None:
            self.setSpatial(matrix)
            #print 'setting matrix'
        
        rbfi = si.Rbf(self.xMatrix, 
                      self.yMatrix, 
                      self.zMatrix)
        return rbfi(x,y)

    

