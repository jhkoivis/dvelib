
import unittest
import numpy
import subprocess
import time

class TestConvolution(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testSimpleTest(self):
        
        tStamp = "dat" #time.time()
        refImgFn = '/tmp/refImg.%s' % (tStamp)
        defImgFn = '/tmp/defImg.%s' % (tStamp)
        sumImgFn = '/tmp/sumImg.%s' % (tStamp)
        xSize = 256
        ySize = 256
        
        refImg = numpy.random.random((xSize, ySize))
        defImg = numpy.random.random((xSize, ySize))
        numpy.savetxt(refImgFn, refImg, "%.7f", delimiter = ',')
        numpy.savetxt(defImgFn, defImg, "%.7f", delimiter = ',')
        
        cmd = './sumImg %s %s %s %d %d' % ( refImgFn,
                                            defImgFn,
                                            sumImgFn,
                                            xSize,
                                            ySize)
        
        subprocess.call(cmd, shell = True)
        
        sumImg = numpy.loadtxt(sumImgFn)
        #print sumImg
        for i in range(xSize):
            for j in range(ySize):
                self.assertAlmostEqual(sumImg[i,j], 
                                       refImg[i,j] + defImg[i,j],
                                       places = 6)
        
if __name__ == '__main__':
    unittest.main()