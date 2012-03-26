
import unittest
from histogram import histogram
import numpy

class TestHistogram(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testOneNumber(self):
        
        out = histogram([1])
        self.assertAlmostEqual(out[0,0], 2)
        self.assertAlmostEqual(out[0,1], 1)  
        
        out = histogram([10])
        self.assertAlmostEqual(out[0,0], 16)
        self.assertAlmostEqual(out[0,1], 0.125)
        
    def testTwoNumbers(self):
        
        out = histogram([1,2])
        self.assertEqual(out[0,0], 2)
        self.assertEqual(out[0,1], 0.5)  
        self.assertEqual(out[1,0], 4)
        self.assertEqual(out[1,1], 0.25)  
        
    def testRealData(self):
        
        dataRaw = numpy.loadtxt('testData/excursionTimes_experiments.dat') 
        data = dataRaw[:,2]
        
        outCorrectRaw = numpy.loadtxt('testData/exp_histo.dat')
        #print numpy.sum((outCorrectRaw[1:,0]-outCorrectRaw[:-1,0])*outCorrectRaw[1:,1])
        outC = outCorrectRaw[outCorrectRaw[:,1] > 0, :]
        
        outSum = numpy.sum(outC[:,1])
        #print numpy.sum(outC[1:,0]*outC[:,1])
        
        out = histogram(data)
        outSum = numpy.sum(out[:,1])
        #print outSum
        outUn = histogram(data, normalize = False)
        
        for i in range(len(out)):
            self.assertAlmostEqual(out[i,0], outC[i,0])
            #print out[i,0], out[i,1]/outC[i,1]
            self.assertAlmostEqual(out[i,1], outC[i,1])
  
    def testUnnormedRealData(self):
        
        dataRaw = numpy.loadtxt('testData/excursionTimes_experiments.dat') 
        data = dataRaw[:,2]
        
        outCorrectRaw = numpy.loadtxt('testData/exp_histo_unnormed.dat')
        outC = outCorrectRaw[outCorrectRaw[:,1] > 0, :]
        
        out = histogram(data, normalize = False)
        counti = 0
        for i in range(len(out)):
            counti += 1
            self.assertAlmostEqual(out[i,0], outC[i,0])
            self.assertAlmostEqual(out[i,1], outC[i,1])
        self.assertEqual(counti, 16)     
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    