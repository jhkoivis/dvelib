
import scipy.interpolate as si
import numpy
import unittest

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

        rbfi = self.getSimpleInterpolatorFunction(x, y, matrix)

        return rbfi(x,y)
    
    def getSimpleInterpolatorFunction(self, x, y, matrix=None):
        if self.xMatrix == None:
            self.setSpatial(matrix)
            #print 'setting matrix'
        
        rbfi = si.Rbf(self.xMatrix, 
                      self.yMatrix, 
                      self.zMatrix)
        
        return rbfi
		
	# def interpolateIndexPoint(self,x,y,mat, debug = 0):
		# """
			# interpolates mat at point.
			# Uses indices as coordinates.
			# X is the first index
		# """
		# # get corners points
		# points = []
		# for fc_x in [np.floor(x), np.floor(x) + 1]:
			# for fc_y in [np.floor(y), np.floor(y) + 1]:
				# points.append([float(fc_x), float(fc_y), mat[fc_x,fc_y]])
		
		# # get distance to given points
		# distMax = 0
		# pointMax = []
		# for point in points:
			# dx = point[0] - x
			# dy = point[1] - y
			# d = dx**2 + dy**2
			# if d >= distMax:
				# pointMax = point
				# distMax = d
		
		# if debug: print points
		# #remove furthest point
		# #print pointMax
		# points.remove(pointMax)
		
		# # get Plane equation: http://paulbourke.net/geometry/planeeq/
		# dMat = [points[0], points[1], points[2]]
		# # detMat indices: index, row, xyz
		# detMats = np.array([dMat,dMat,dMat,dMat])
		# coefs = np.array([0.0,0.0,0.0,0.0])

		# for i in range(4):
			# try:
				# detMats[i,:,i] = 1.0
			# except:
				# # i = 4 : dMat = -dMat
				# detMats[i,:,:] *= -1.0
			# matrix = np.array(detMats[i,:,:])
			# coefs[i] = np.linalg.det(matrix)
			# if debug: print matrix
		# coefs = map(float, coefs)
		# if debug: print detMats
		# if debug: print coefs
		# # ax + by + cz + d = 0
		# # z = -(ax + by + d)/c
		
		# #if coefs[2] == 0: return 0
		# return -(coefs[0]*x + coefs[1]*y + coefs[3])/float(coefs[2])

		# #xVect = np.arange(mat.shape[0])
		# #yVect = np.arange(mat.shape[1])
		# #z = mat
		# #f = interpolate.interp2d(xVect, yVect, z, kind='cubic')
		# #return f(x,y)

		
		
		

class TestInterp2D(unittest.TestCase):
    
    def testSameAtNodes(self):
        i = Interp2D()
        r = numpy.random.random((10,10))
        for x in range(10):
            for y in range(10):
                out = i.simple(x, y, r)
                try:
                    self.assertAlmostEqual(out,r[x,y], places = 5)
                except AssertionError:
                    print x,y
                    raise
                
    def testSimplePlane(self):
        i = Interp2D()
        y, x = numpy.meshgrid(range(11), range(11))
        z = 0.5*x + 0.5*y
        
        out = float(i.simple(5,5,z))
        self.assertAlmostEqual(5, out)
        
        for index in range(100):
            x = numpy.random.random((1,)) * 11
            y = numpy.random.random((1,)) * 11
            correct = 0.5*float(x) + 0.5*float(y)
            out = float(i.simple(x,y,z))
            self.assertAlmostEqual(correct, out, places = 0)
            
            
    def testPreVectors(self):
        y, x = numpy.meshgrid(range(11), range(11))
        z = 0.5*x + 0.5*y
        i = Interp2D(matrix=z)
       
        out = float(i.simple(5,5,z))
        self.assertAlmostEqual(5, out) 
    

