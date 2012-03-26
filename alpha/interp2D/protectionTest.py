import inspect



class ProtectionTest:
    
    __myPrivate = 0
    
    def __init__(self):
        md = myDict()
        setattr(self,'__dict__', md)
        
    def __setattr__(self, name, val):     
        if name == '__myPrivate':
            print "failed setattr attempt: __myPrivate"
            pass
        elif name == '_ProtectionTest__myPrivate':
            print "failed setattr attempt: _ProtectionTest__myPrivate"  
            pass
        elif name == '__dict__':
            print "failed setattr attempt: __dict__"
            pass
        else: 
            self.__dict__[name] = val             

    def getMyPrivate(self):
        return self.__myPrivate
    
    def setMyPrivate(self, myPrivate):
        #self.__dict__['_ProtectionTest__stack'] = inspect.stack()[0][1:]
        self.__dict__['_ProtectionTest__myPrivate'] = -myPrivate


class myDict(dict):
    
    def __init__(self):
        dict.__init__(self)
    
    def __setitem__(self, key, value):
        
        if inspect.stack()[1][3] == 'setMyPrivate':
            dict.__setitem__(self,key,value)
        else:
            print "failed dict attempt"
            pass

pt = ProtectionTest()
setattr = 0

print "trying to change... (success: 1): "
pt.__myPrivate = 1
print pt.getMyPrivate(), '\n'

print "trying to change... (success: 2): "
pt._ProtectionTest__myPrivate = 2
print pt.getMyPrivate() , '\n'

print "trying to change... (success: 3): "
pt.__dict__.__setitem__('_ProtectionTest__myPrivate', 3)
print pt.getMyPrivate() , '\n'

print "trying to change the function (success: 4): "
def setMyPrivate(self, myPrivate):
    self.__dict__['_ProtectionTest__myPrivate'] = 4
pt.setMyPrivate = setMyPrivate
pt.setMyPrivate(0)
print pt.getMyPrivate(), '\n'

print "trying to change the function (success: 4): "
def setMyPrivate(self, myPrivate):
    self.__dict__['_ProtectionTest__myPrivate'] = 4
setattr(pt.setMyPrivate,setMyPrivate)
pt.setMyPrivate(0)
print pt.getMyPrivate(), '\n'

print "trying to change the dict (success: 5): "
pt.__dict__ = {}
pt.__dict__.__setitem__('_ProtectionTest__myPrivate',5)
print pt.getMyPrivate(), '\n'



print "Still working (correct output = -input = -100): "    
pt.setMyPrivate(100)
print pt.getMyPrivate()  
    
    
    
    
    