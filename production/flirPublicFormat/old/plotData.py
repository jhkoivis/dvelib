
import matplotlib
matplotlib.use('macOSX')
import pylab
from pylab import *
import numpy

a = numpy.loadtxt('data.dat')

b = reshape(a[0:-1],(240,320))

imshow(b, vmin=295, vmax=296)
colorbar()
#caxis([295,296])

show()