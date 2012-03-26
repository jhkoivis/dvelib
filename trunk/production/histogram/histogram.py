
import numpy

def histogram(data, abskissa = None, normalize = True):
    
    # set abskissa (bins)
    if abskissa == None:
        ind = numpy.arange(-100,100)
        abskissa = numpy.power(2.0, ind)
    # indices of abskissa
    mIndex = numpy.array(range(len(abskissa)))
    
    # index of correct bin
    out = numpy.zeros(len(abskissa) - 1)
    for d in data:
        ind = mIndex[d < abskissa[:-1]][0]
        out[ind] += 1.0
    
    # normalize: sum_i bin_i*height_i = 1
    if normalize:
        sumOut = 0.0
        for i in range(len(out)):
            sumOut += out[i]
        out = out/sumOut
        for i in range(len(out)):
            da = abskissa[i] - abskissa[i-1]
            #print out[i], da, abskissa[i]
            out[i] = out[i] / da
            #sumOut += out[i]
        #out = out/sumOut
        
    ind = out > 0.0
    return numpy.array([abskissa[ind], out[ind]]).T





