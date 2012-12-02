
from main import *

bp = Blueprint()
#v = Vectors()

#bp.loadImage('pentagram.bmp')
bp.loadImage('lizard2.png')
bp.imageToBinary()
bp.binaryToVectors()


v = Vectors()
v.setPoints(bp.vectorList2)
v.divideIntoPieces()


bp.showImage()
v.smooth()
v.plotParts()
pylab.show()

