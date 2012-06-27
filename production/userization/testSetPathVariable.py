
import unittest
import setPathVariable

class TestSetPathVariable(unittest.TestCase):
    
    def testGetOldPath(self):
        spv = setPathVariable.SetPathVariable()
        print spv.winGetOldPath()
    
    def testSetNewPath(self):
        spv = setPathVariable.SetPathVariable()
        path = spv.winGetOldPath()
        spv.winSetNewPath(path)
        path2 = spv.winGetOldPath()
        self.assertEqual(path,path2)