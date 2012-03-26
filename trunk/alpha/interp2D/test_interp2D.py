

import interp2D
import unittest
import numpy
import pylab

class TestCase(unittest.TestCase):
    
    def testSameAtNodes(self):
        i = interp2D.Interp2D()
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
        i = interp2D.Interp2D()
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
        i = interp2D.Interp2D(matrix=z)
       
        out = float(i.simple(5,5,z))
        self.assertAlmostEqual(5, out) 
        
            
            
            
            
            