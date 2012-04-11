import pylab
from pylab import *
import numpy as np

manXnames = np.array(range(0,120))
Ynames = (8.3333333333333331e-05)*manXnames + 0.01
Vt_X = manXnames
Vt_Y = (12.0/1000.0)*np.exp(-0.01*(120-manXnames))
Vterror = Ynames + randn(size(Ynames))

fig_base = pylab.figure()
fig1 = fig_base.add_subplot(111)
lns1 = fig1.plot(manXnames, Ynames, marker='s', color='g',label='Plain Line')
lns2 = fig1.plot(Vt_X, Vt_Y, marker='^', color='r',label='V_t')

# yticks on left
locs,labels = yticks()
pylab.yticks(locs, map(lambda x: "%g" % x, locs*1e3))

#axis labels
pylab.xlabel('Temperature (C)') 
pylab.ylabel('Emitter Voltage (mV)', labelpad=20)
pylab.xticks(rotation=45)

pylab.legend()
fig2 = fig1.twinx()
lns3 = fig2.plot(manXnames, Vterror, marker='o', linestyle='-',label='V_terror') 

# xticks
locs,labels = xticks()
pylab.xticks(locs, map(lambda x: "%g" % x, locs))

# yticks on right
locs,labels = yticks()
pylab.yticks(locs, map(lambda x: "%g" % x, locs))

#2nd axis labels    
pylab.ylabel('Percentage Error %', labelpad=20)

pylab.legend(loc="lower right")
pylab.show()