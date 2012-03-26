
import unittest
import copySshKeys

class testCopySshKeys(unittest.TestCase):
    
    def Setup(self):
        """
            Nothing
        """
        a = 1
        
    def testLoadClass(self):
        """
        loads copySshKeys.py
        """
        csk = copySshKeys.copySshKeys()
        
    def testMakeLocalKeys(self):
        """
        creates local key, check if it produces id_rsa and id_rsa.pub
        """
        csk = copySshKeys.copySshKeys()
        csk.makeLocalKeys()
        