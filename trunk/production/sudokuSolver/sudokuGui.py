
import pylab
import numpy
import subprocess
from matplotlib.font_manager import FontProperties

font0 = FontProperties()

def drawGrid():
    for i in [5, 35, 65, 95]:
        pylab.plot([i,i],[5,95],'k-')
        pylab.plot([5,95], [i,i],'k-')

def getInitial(fn):
    for line in open(fn):
        font0.set_weight('bold')
        try:
            print line.replace('paint','').split('.')[0]
            numTuple = eval(line.replace('paint','').split('.')[0])
            pylab.text(numTuple[0]*10, 
                       numTuple[1]*10, 
                       numTuple[2], 
                       fontproperties = font0)
        except:
            print line
            pass

def solveSudoku(fn):
    cmd = "clingo.exe sudoku.lp %s" % (fn)
    
    a = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    
    sudokuArray = numpy.zeros((9,9))
    sudokuList = []
    
    results = a.stdout.readlines()
    print results
    
    for number in results[1].split('paint'):
        try:
            numTuple = eval(number)
            x,y,value = numTuple
            sudokuArray[x-1,y-1] = value
            sudokuList.append(numTuple)
            pylab.text(x*10, y*10, value)
        except:
            pass
    
    pylab.plot([0,0],[0,100],'ro-')
    pylab.plot([0,100],[100,100], 'ro-')
    pylab.show()



fn = 'sudo-wiki.lp'
drawGrid()
getInitial(fn)
solveSudoku(fn)

    
    