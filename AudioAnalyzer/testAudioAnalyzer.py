
import AudioAnalyzer
import unittest
import array

class TestAudioAnalyzer(unittest.TestCase):
    
    def setUp(self):
        
        self.testFile1 = 'testData/horse.wav'
        self.testOutFile1 = 'testData/horse.mp3'
        self.aa = AudioAnalyzer.AudioAnalyzer()

    def testConvertToWavWithExternal(self):
        """
        TODO
        """
        infile = self.testFile1
        outfile = self.testOutFile1
        exitCode = self.aa.convertToWavWithExternal(infile,outfile)
        self.assertEqual(0,exitCode)
    
    def testLoadfile(self):
        """
        TODO
        """
        file = self.aa.loadAudioFile(self.testFile1)
        
    def testSaveFile(self):
        """
        Load test file convert it to array and save as wav.
        """
        file = self.aa.loadAudioFile(self.testFile1)
        
        
    def testPrintAudio(self):
        """
        Print audio as ascii series
        """
        f = self.aa.loadAudioFile(self.testFile1)
        t = f.getparams()
        SampleRate = t[2]
        data = array.array("h", f.readframes(t[3]))
        #for line in data:
        #    print line
        #print self.aa.getAudioAsArray(file)
        