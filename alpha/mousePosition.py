from Xlib import X, display
import time

d = display.Display().screen().root.query_pointer()._data

print "x="+str(d["root_x"])
print "y="+str(d["root_y"])