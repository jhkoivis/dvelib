import btsocket
import asyncore
ap_id = btsocket.select_access_point()
apo = btsocket.access_point(ap_id)
apo.start()
print "PHONE IP IS", apo.ip()