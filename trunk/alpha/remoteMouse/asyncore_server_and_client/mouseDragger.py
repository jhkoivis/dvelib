
import win32api, win32con
import time

class MouseDragger:

    def leftClick(self,x,y):
        #(x0,y0) = win32api.GetCursorPos()
        #x+= x0
        #y+= y0
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        
    def leftDrag(self, pointList):
        
        x0 = 200
        y0 = 200
        x = x0 + pointList[0][0]
        y = y0 + pointList[0][1]
        
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        for i in range(len(pointList) - 1):
            dx = pointList[i+1][0] - pointList[i][0]
            dy = pointList[i+1][1] - pointList[i][1]
            x = pointList[i+1][0] + x0
            y = pointList[i+1][1] + y0
            #print dx, dy
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,dx,dy,0,0)
            win32api.SetCursorPos((x,y))
            time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        
    def parseString(self, s):
        s = s.split(';')[-1]
        ss = s.split(',')
        pointList = []
        for i in range(len(ss)-1):
            if i % 2  == 0:
                x = int(ss[i])
            else:
                y = int(ss[i])
                pointList.append([x,y])
        return pointList

md = MouseDragger()
md.leftDrag([[500,500], [400,300], [400,300], [300,300]])
    
s = '152;365,129,363,129,356,129,341,129,308,134,278,144,255,161,241,181,231,204,230,224,231,234,240,241,245,243,256,243,265,239,271,236,276,233,280,231,281,229,'
pl = md.parseString(s)
#md.leftDrag(pl)

 
#click(10,10)