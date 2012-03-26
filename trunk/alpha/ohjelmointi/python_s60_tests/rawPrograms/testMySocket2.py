
import unittest
import mySocket
import asyncore

class TestMySocket(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testInit(self):
        c = mySocket.MySocketClient("", 12345)
        asyncore.loop()
        
if __name__ == '__main__':
    unittest.main()