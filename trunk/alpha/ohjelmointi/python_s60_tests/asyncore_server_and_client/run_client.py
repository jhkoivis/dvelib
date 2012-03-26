
import asyncore

import mySocket
import time
#a = mySocket.MyService(12345)
#a.start()

#b = mySocket.MyClient("", 12377, verbose = 1)
#b.start()

b = mySocket.MySocketClient("",12377, verbose = 1)
asyncore.loop()


#a.quit()
