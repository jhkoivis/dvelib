
fn = "colors.eps"

inFile = open(fn, "r")
maxLine = 64

# aalto colors
yellow = "{%f %f %f}" %     (254.0/255, 203.0/255,  0.0/255) 
red = "{%f %f %f}" %        (237.0/255, 41.0/255,   57.0/255)  # 0.9294 0.1608 0.2235
blue = "{%f %f %f}" %       (0.0/255,   101.0/255,  189.0/255) # 0      0.3961 0.7412
black = "{%f %f %f}" %      (0.0/255,   0.0/255,    0.0/255)
gray = "{%f %f %f}" %       (146.0/255, 139.0/255,  129.0/255)
lgreen = "{%f %f %f}" %     (105.0/255, 190.0/255,  40.0/255)
green = "{%f %f %f}" %      (0.0/255,   155.0/255,  58.0/255)
lblue = "{%f %f %f}" %      (0.0/255,   168.0/255,  180.0/255)
violet = "{%f %f %f}" %     (102.0/255, 57.0/255,   183.0/255)
purple = "{%f %f %f}" %     (177.0/255, 5.0/255,    157.0/255)
orange = "{%f %f %f}" %     (255.0/255, 121.0/255,  0.0/255)

currentLine = 0
for line in inFile:
    currentLine += 1
    if currentLine < maxLine:
        if line[:8].strip() == "/Color2":
            print "/Color2 %s def" % (red)
        elif line[:8].strip() == "/Color3":
            print "/Color3 %s def" % (lgreen)
        elif line[:8].strip() == "/Color4":
            print "/Color4 %s def" % (blue)
        elif line[:8].strip() == "/Color5":
            print "/Color5 %s def" % (yellow)
        #elif line[:8].strip() == "/Color6": # brown
        #    print "/Color6 %s def" % (lgreen)
        elif line[:8].strip() == "/Color7":
            print "/Color7 %s def" % (gray)
        elif line[:8].strip() == "/Color8":
            print "/Color8 %s def" % (violet)
        #elif line[:8].strip() == "/Color9": # cyan
        #    print "/Color9 %s def" % (purple)
        elif line[:8].strip() == "/Color10": 
            print "/Color10 %s def" % (purple)
        elif line[:8].strip() == "/Color11":
            print "/Color11 %s def" % (orange)
        #elif line[:8].strip() == "/Color12": # indigo
        #    print "/Color12 %s def" % ()
        #elif line[:8].strip() == "/Color13": # maroon
        #    print "/Color13 %s def" % (orange)
        #elif line[:8].strip() == "/Color14": # turquioise
        #    print "/Color14 %s def" % (orange)
        elif line[:8].strip() == "/Color15":
            print "/Color15 %s def" % (green)
        else:
            print line
    else:
        print line
# white
# /Color0 {1.0000 1.0000 1.0000} def 
# black
#/Color1 {0.0000 0.0000 0.0000} def
#/Color2 {1.0000 0.0000 0.0000} def
#/Color3 {1.0000 1.0000 0.0000} def
#/Color4 {0.0000 0.0000 1.0000} def
#/Color5 {1.0000 1.0000 0.0000} def
#/Color6 {0.7373 0.5608 0.5608} def
#/Color7 {0.8627 0.0 0.8627} def
#/Color8 {0.5804 0.0000 0.8275} def
#/Color9 {0.0000 1.0000 1.0000} def
#/Color10 {1.0000 0.0000 1.0000} def
#/Color11 {1.0000 0.6471 0.0000} def
#/Color12 {0.4471 0.1294 0.7373} def
#/Color13 {0.4039 0.0275 0.2824} def
#/Color14 {0.2510 0.8784 0.8157} def
#/Color15 {0.0000 0.5451 0.0000} def
#/Color16 {0.7529 0.7529 0.7529} def
#/Color17 {0.5059 0.0 0.5059} def
#/Color18 {0.2588 0.0 0.2588} def




