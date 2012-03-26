import numpy
import pylab
import pickle

from glob import glob

def loadTtm(data, fnGlobPattern = 'D:\woodSize\*[0-9]'):
    fnList = glob(fnGlobPattern)
    fnList.sort()
    #print fnList
    for fn in fnList:
        expid = fn.split('_')[-1].encode('utf-8').lower().strip()
        print expid
        if data.has_key(expid):
            #print expid, ' found'
            ttmData = numpy.loadtxt(fn)
            data[expid]['ttmData'] = ttmData[::100]
                       
def loadMeasured(data, 
                 dimensionFn = 'WoodSamplesSize.xls',
                 excelFirstRow = 8):
    import sys
    sys.path.append('U:\\\\Documents\\pythonPackages\\Lib\\site-packages')
    import xlrd
    
    doc = xlrd.open_workbook(dimensionFn)
    sheet = doc.sheet_by_index(0)

    #for i in range(sheet.ncols):
    #    print i, sheet.cell_value(0,i)
    #print excelFirstRow
    for i in range(excelFirstRow ,sheet.nrows):
        #print sheet.cell_value(i,1)
        try:
            expid = sheet.cell_value(i,1).encode('utf-8').lower().strip()
        except AttributeError: # cell_value is float, not string 
            expid = str(int(sheet.cell_value(i,1)))
#        w1 = sheet.cell_value(i,3)
#        w2 = sheet.cell_value(i,4)
#        w3 = sheet.cell_value(i,5)
#        if w2 == "": w2 = w1
#        if w3 == "": w3 = w1
#        width = [w1,w2,w3]
        width = [sheet.cell_value(i,3),
                 sheet.cell_value(i,4),
                 sheet.cell_value(i,5)]
        depth = [sheet.cell_value(i,6),
                 sheet.cell_value(i,7),
                 sheet.cell_value(i,8)]
        height = [sheet.cell_value(i,9),
                 sheet.cell_value(i,10),
                 sheet.cell_value(i,11)]
        data[expid] = {'widthArray'     : width,
                       'heightArray'    : height,
                       'depthArray'     : depth}
  
def loadData(data, 
         fnTtmGlobPattern = 'D:\work\tampere\woodSize\2011*', 
         fnDimensionExcel = 'tampere-experiments-dimensions.xls',
         excelFirstRow = 8):
    loadMeasured(data, 
                 dimensionFn = fnDimensionExcel,
                 excelFirstRow = excelFirstRow)
    expidList = data.keys()
    expidList.sort()
    loadTtm(data, fnGlobPattern=fnTtmGlobPattern)
    pickle.dump(data, open('data.pikled', 'wb'))

def plotForceDisplacement(data):
    for id, dataDict in data.iteritems():
        #if not id.find('s04-') == 0: continue
        #symbol = '.'
        #if id.find('-05-') > 0: symbol = 'r-'   
        #if id.find('-10-') > 0: symbol = 'g-'
        #if id.find('-20-') > 0: symbol = 'b-'
        #if id.find('-40-') > 0: symbol = 'm-'
        #if id.find('-80-') > 0: symbol = 'c-'
        
        
        try:
            label = "area = %f mm2, %s" % (100*100*100*getArea(dataDict), id)
            force = getForce(dataDict)
            disp = getDisp(dataDict)
            pylab.plot(disp, force, label = label)
        except:
            #raise
            pass
    
    pylab.xlabel('Displacement [mm]')
    pylab.ylabel('Force [N]')
    pylab.legend(loc = 'upper left')
    pylab.show()
    
def getDisp(dataDict): 
    force = getForce(dataDict)
    disp = -dataDict['ttmData'][:,2]*1000.0
    return disp[:force.shape[0]]

def getForce(dataDict):
    #print dataDict 
    force = -dataDict['ttmData'][:,1]*1000.0
    maxForceInd = numpy.argmax(force)
    return force[:maxForceInd]

def getStrain(dataDict, yieldStressEstimateInNewtons = 280):
    
    disp = getDisp(dataDict)
    #print disp
    disp = disp - getDispZero(dataDict, 
                              yieldStressEstimateInNewtons = yieldStressEstimateInNewtons)
    #print disp
    height = numpy.mean(dataDict['heightArray'])
    
    strain = disp/height
    
    return strain

def getStress(dataDict):
    
    area = numpy.mean(dataDict['widthArray'])/1000.0
    area *= numpy.mean(dataDict['depthArray'])/1000.0
    force = getForce(dataDict)
    
    stress = force/area
    
    return stress

def interpDispForce(dataDict, debug = False):
    disp    = getDisp(dataDict)
    force   = getForce(dataDict)
    disp    = disp[:numpy.argmax(force)]
    force   = force[:numpy.argmax(force)] 
    
    dispInterp  = numpy.arange(numpy.min(disp), numpy.max(disp), 0.01)
    forceInterp = numpy.interp(dispInterp, disp, force, 2)
    
    if debug:
        return dispInterp, forceInterp, disp, force
    
    return dispInterp, forceInterp

def testInterpDispForce(dataDict):
    
    di, fi, d, f = interpDispForce(dataDict, debug = True)
    
    pylab.plot(d,f, label = 'original')
    pylab.plot(di,fi, 'ro', label = 'interpolated')
    pylab.legend()
    pylab.show()
    
def getYoungDispForceAndSlope(dataDict, lag = 2, debug = False, 
                              yieldStressEstimateInNewtons = 280):
    forceCutInN = yieldStressEstimateInNewtons
    disp, force = interpDispForce(dataDict)
    #force = dataDict['ttmData'][:,2]*1000.0
    disp = disp[force < forceCutInN]
    force = force[force < forceCutInN]
    #print disp
    #print force
    cs = numpy.cumsum(force)
    
    raForce = (cs[lag:] - cs[:-lag])/lag
    raDisp = disp[lag/2:-lag/2]
    
    derForce = (raForce[lag:] - raForce[:-lag])/(raDisp[lag:] - raDisp[:-lag])
    derDisp = raDisp[lag/2:-lag/2]
    
    ind = numpy.argmax(derForce)
    derMax = numpy.max(derForce)
    youngDisp = derDisp[ind]  
    youngForce = force[disp >= youngDisp][0] 
    
    if debug:
        return youngDisp, youngForce, raForce, raDisp, derForce, derDisp, disp, force
    
    return youngDisp, youngForce, derMax

def testGetYoungDispAndForce(dataDict):
    
    youngDisp, youngForce, raForce, raDisp, derForce, derDisp, disp, force = getYoungDispAndForce(dataDict, debug = True)
    
    pylab.plot(youngDisp, youngForce, 'ro', label = 'Young Point')
    pylab.plot(raDisp, raForce, 'g', label = 'running average')
    pylab.plot(derDisp, derForce, 'b', label = 'derivative')
    pylab.plot(disp, force, 'k', label = 'cutted original')
    pylab.legend()
    pylab.show()

def getDispZero(dataDict, yieldStressEstimateInNewtons = 280):
    try:
        youngDisp, youngForce, derForce = getYoungDispForceAndSlope(dataDict,yieldStressEstimateInNewtons = yieldStressEstimateInNewtons)
        dispZero = youngDisp - youngForce/derForce
    except:
        print "Young modulus method failed: using first point as strain zero."
        print "getDispZero: ", getDisp(dataDict)
        print "getDispZero: ", numpy.min(getDisp(dataDict))
        return numpy.min(getDisp(dataDict))
    
    return dispZero
        
def testGetDispZero(dataDict):
        
    disp, force = interpDispForce(dataDict)
    youngDisp, youngForce, derForce = getYoungDispForceAndSlope(dataDict)
    
    k = derForce
    b = youngForce - k * youngDisp
    
    testData = numpy.polyval([k,b], disp)
    
    dispZero = getDispZero(dataDict)
    
    pylab.plot(disp,force)
    pylab.plot(disp,testData)
    pylab.plot(dispZero, 0, 'ro')
    pylab.show()
       
def plotStressStrain(data, yieldStressEstimateInNewtons = 280):
    for id, dataDict in data.iteritems():
        #if not id.find('s04-') == 0: continue
        symbol = '.'
        #if id.find('-05-') > 0: symbol = 'r-'   
        #if id.find('-10-') > 0: symbol = 'g-'
        #if id.find('-20-') > 0: symbol = 'b-'
        #if id.find('-40-') > 0: continue #symbol = 'm-'
        #if id.find('-80-') > 0: continue #symbol = 'c-'
        
        try:
            label = "area = %f mm2, %s" % (100*100*100*getArea(dataDict), id)
            stress = getStress(dataDict)
            strain = getStrain(dataDict, yieldStressEstimateInNewtons = yieldStressEstimateInNewtons)
            pylab.plot(strain, stress/1e6, symbol, label = label)
        except:
            #raise
            pass
    
    pylab.xlabel('Strain [unitless]')
    pylab.ylabel('Stress [GPa]')
    pylab.legend(loc = 'upper left')
    pylab.show()
    
def plotStressStrain_cleaned(data):
    for id, dataDict in data.iteritems():
        if not id.find('s04-') == 0: continue
        symbol = 'k-'
        if id.find('-05-') > 0: symbol = 'r-'   
        if id.find('-10-') > 0: symbol = 'g-'
        if id.find('-20-') > 0: symbol = 'b-'
        if id.find('-40-') > 0: continue
        if id.find('-80-') > 0: continue
        
        try:
            stress = getStress(dataDict)
            strain = getStrain(dataDict)
            pylab.plot(strain, stress/1e6, symbol, label = id)
        except:
            raise
            pass
    
    pylab.xlabel('Strain [%/100]')
    pylab.ylabel('Stress [GPa]')
    pylab.legend(loc = 'upper left')
    pylab.show()
  
def plotStressStrain_shifted(data, blacklist = []):
    for id, dataDict in data.iteritems():
        if blacklist.__contains__(id): continue
        
        if not id.find('s04-') == 0: continue
        symbol = 'k-'
        if id.find('-05-') > 0: symbol = 'r-'   
        if id.find('-10-') > 0: symbol = 'g-'
        if id.find('-20-') > 0: symbol = 'b-'
        if id.find('-40-') > 0: continue
        if id.find('-80-') > 0: continue
        
        try:
            stress = getStress(dataDict)
            strain = getStrain(dataDict)
            strain = strain - numpy.max(strain)
            pylab.plot(strain, stress/1e6, symbol, label = id)
        except:
            raise
            pass
    
    pylab.xlabel('Strain [%/100]')
    pylab.ylabel('Stress [GPa]')
    pylab.legend(loc = 'upper left')
    pylab.show()
    
def plotStressStrain_scaled(data, blacklist = []):
    for id, dataDict in data.iteritems():
        if not id.find('s04-') == 0: continue
        symbol = 'k-'
        
        if blacklist.__contains__(id): continue
        
        if id.find('-05-') > 0: symbol = 'r-'   
        if id.find('-10-') > 0: symbol = 'g-'
        if id.find('-20-') > 0: symbol = 'b-'
        if id.find('-40-') > 0: continue # symbol = 'm-'
        if id.find('-80-') > 0: continue # symbol = 'c-'
        
        try:
            stress = getStress(dataDict)
            strain = getStrain(dataDict)
            strain = strain/numpy.max(strain)
            pylab.plot(strain, stress/1e6, symbol, label = id)
        except:
            raise
            pass
    
    pylab.xlabel('Strain [%/100]')
    pylab.ylabel('Stress [GPa]')
    pylab.legend(loc = 'upper left')
    pylab.show()
 
def plotYoungModulusAgainstHeight(data, blacklist = []):
    for id, dataDict in data.iteritems():
        try:
            if blacklist.__contains__(id): continue
            young = getYoungModulus(dataDict)/1e9
            height = getHeight(dataDict)
            pylab.plot(height, young, 'o')
            print height, young
        except:
            
            pass
    pylab.xlabel('Height [mm]')
    pylab.ylabel('Young Modulus [GPa]')
    pylab.show()
    


def getArea(dataDict):
    area = numpy.mean(dataDict['widthArray'])/1000.0
    area *= numpy.mean(dataDict['depthArray'])/1000.0

    return area

def getHeight(dataDict):
    height = numpy.mean(dataDict['heightArray'])
    
    return height

def getYoungModulus(dataDict):
    d,f,der = getYoungDispForceAndSlope(dataDict)
    
    # der = Delta force / Delta displacement
    # young Mod = Delta stress / delta strain =  (deltaforce/area) / (deltadisp/height) = height/area * deltaforce / deltadisp
     
    young = der/getArea(dataDict)*getHeight(dataDict)
    
    return young

def testYoungModulus(dataDict):
    
    stress = getStress(dataDict)
    strain = getStrain(dataDict)
    young = getYoungModulus(dataDict)
    straight = numpy.polyval([young,0], strain)
    pylab.plot(strain, stress)
    pylab.plot(strain, straight)
    pylab.show()
    
    pass
  
pass
   
def getSlopes(dataDict):
    
    stress = getStress(dataDict)
    strain = getStrain(dataDict)
    
    params = []
    dataLen = stress.shape[0]
    for i in range(4):
        minInd = int(dataLen/4 * i)
        maxInd = int(dataLen/4 * (i+1))
        stressPart = stress[minInd:maxInd]
        strainPart = strain[minInd:maxInd]
        
        p = numpy.polyfit(strainPart,stressPart,1)
        
        params.append(p)
        
    return params

def getSlope2Per4(dataDict):
    
    params = getSlopes(dataDict)
    slope2 = params[1][0]
    
    return slope2

def getSlope4Per4(dataDict):
    params = getSlopes(dataDict)
    slope2 = params[3][0]
    
    return slope2
 
def plotSlope2AgainstHeight(dataDict, blacklist = []):
    for id, dataDict in data.iteritems():
        try:
            if blacklist.__contains__(id): continue
            second = getSlope2Per4(dataDict)
            height = getHeight(dataDict)
            pylab.plot(height, second, 'o')
            print height, second
        except:   
            pass
    pylab.xlabel('Height [mm]')
    pylab.ylabel('Slope 2/4 [unitless]')
    pylab.show()
 
def plotSlope4AgainstHeight(dataDict, blacklist = []):
    for id, dataDict in data.iteritems():
        try:
            if blacklist.__contains__(id): continue
            second = getSlope4Per4(dataDict)
            height = getHeight(dataDict)
            pylab.plot(height, second, 'o')
            print height, second
        except:   
            pass
    pylab.xlabel('Height [mm]')
    pylab.ylabel('Slope 4/4 [unitless]')
    pylab.show()
    
def plotYieldStressAgainstHeight(dataDict, blacklist = []):
    for id, dataDict in data.iteritems():
        try:
            if blacklist.__contains__(id): continue
            yp = getYieldPoint(dataDict)
            height = getHeight(dataDict)
            pylab.plot(height, yp[1], 'o')
        except:   
            pass
    pylab.xlabel('Height [mm]')
    pylab.ylabel('Yield Stress [Pa]')
    pylab.show()
    
def plotYieldStrainAgainstHeight(dataDict, blacklist = []):
    for id, dataDict in data.iteritems():
        try:
            if blacklist.__contains__(id): continue
            yp = getYieldPoint(dataDict)
            height = getHeight(dataDict)
            pylab.plot(height, yp[0], 'o')
            print yp[0]
        except:
            #raise   
            pass
    pylab.xlabel('Height [mm]')
    pylab.ylabel('Yield Strain [unitless]')
    pylab.show()
 
def testGetSlopes(dataDict):
    
    params = getSlopes(dataDict)
    strain = getStrain(dataDict)
    stress = getStress(dataDict)
    
    pylab.plot(strain, stress)
    for p in params:
        stress2 = numpy.polyval(p, strain)
        pylab.plot(strain, stress2)
    
    slope2 = getSlope2Per4(dataDict)
    stress3 = pylab.polyval([slope2,0],strain)
    pylab.plot(strain, stress3)
    
    pylab.show()
    
def getYieldPoint(dataDict):
    #d,f,der = getYoungDispForceAndSlope(dataDict)
    #disp = getDisp(dataDict)
    #force = getForce(dataDict)
    
    stress = getStress(dataDict)
    strain = getStrain(dataDict)
    young = getYoungModulus(dataDict)
    straight = numpy.polyval([young,0], strain)
    
    indices = numpy.arange(strain.shape[0])
    
    #print straight
    #print stress
    yieldIndex = indices[straight > 1.15 * stress][0]
    
    return strain[yieldIndex], stress[yieldIndex], strain, straight

def testYieldPoint(dataDict):
    
    strain = getStrain(dataDict)
    stress = getStress(dataDict)
    yp = getYieldPoint(dataDict)
    
    pylab.plot(strain, stress)
    pylab.plot(yp[0],yp[1], 'ro')
    pylab.plot(yp[2], yp[3])
    
    pylab.show()
   
 
        
#data = {}
#loadData(data, fnGlobPattern = '')
#data = pickle.load(open('data.pikled', 'rb'))
#plotForceDisplacement(data)
#plotStressStrain(data)      
#plotStressStrain_shifted(data, blacklist = ['s04-20-02','s04-05-02', 's04-05-01', 's04-10-03', 's04-10-01','s04-20-03'])
#plotStressStrain_scaled(data, blacklist = ['s04-20-02','s04-05-02', 's04-05-01', 's04-10-03'])
#plotYoungModulusAgainstHeight(data)
#plotSlope2AgainstHeight(data)
#plotSlope4AgainstHeight(data)
#plotYieldStressAgainstHeight(data)


#testYieldPoint(data['s04-10-01'])
#testGetSlopes(data['s04-10-01'])
#testYoungModulus(data['s04-10-01'])
#testGetYoungDispAndForce(data['s04-10-01'])
#testInterpDispForce(data['s04-10-01'])
#testGetDispZero(data['s04-10-01'])



















