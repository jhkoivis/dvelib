
from pylab import *
from numpy import *

from glob import glob

def readP2Header(line, header, data):
    
    for item in line.strip().split():
        print item
        if header['p2'] == None:
            header['p2'] = item
            continue
        if header['xSize'] == None:
            header['xSize'] = int(item)
            continue
        if header['ySize'] == None:
            header['ySize'] = int(item)
            continue
        if header['maxVal'] == None:
            header['maxVal'] = float(item)
            continue
        data.append(int(item))

    return (header, data)

def readP2Data(file):
    
    file.seek(0)
   
    header = {'p2'      : None,
              'maxVal'  : None,
              'xSize'   : None,
              'ySize'   : None}
    
    data = []
    for line in file:
        line = line.split('#')[0]
        if header.values().__contains__(None):
            (header,data) = readP2Header(line, header, data)
            continue
        for item in line.strip().split():
            data.append(float(item))
    print data[1:10]
    data = reshape(data, (header['ySize'], header['xSize']))
    
    return (data, header)

def readImage(fn):
    
    try:
        data = imread(fn)
    except IOError:
        # PIL does not know how to handle
        file = open(fn,'r')
        line = file.readline()
        if line[:2] == 'P2':
            return readP2Data(file)
        else:
            raise
    
    return array(data)

min0 = None
max65535 = None

for fn in sorted(glob('/work/jko/polycarbonate/test_18/*00.fpf.pgm')):
    
    file = open(fn, 'r')
    
    for line in file:
        if not line.strip()[0] == '#': continue
        if line.find('conversion_0_in_celcius') >= 0: 
            min0 = float(line.split(':')[1].strip())
            #if not max65535 == None: 
            #    print 'breaking min0'
            #    break
        if line.find('conversion_65535_in_celsius') >= 0:
            #print line
            max65535 = float(line.split(':')[1].strip())
            #if not min0 == None: break
    
    (data, header) = readImage(fn)
    print data
    imshow(data/65535*max65535 + min0, vmin = 20, vmax = 24)
    colorbar()
    show()
    
    
    
    
    
    
    
    
    
    
    
    