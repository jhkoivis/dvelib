
import unittest
import mySocket
import asyncore
import time

class TestMySocket(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
    
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testInit(self):
        s = mySocket.MyDaemon(12347)
        s.start()
        
        c = mySocket.MySocketClient("", 12347)
        
        #time.sleep(2)
        
        #ss.quit()
        
        c = mySocket.MySocketClient("", 12347)
        
        #time.sleep(2)
        
        
if __name__ == '__main__':
    unittest.main()