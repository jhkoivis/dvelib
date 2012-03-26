import socket as _socket

isConnected = 0
_sockobj = None


def connect(_serverHost, _serverPort):
    'opens a connection to LabVIEW Server'
    global _sockobj, isConnected
    _sockobj = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)      # create socket
    try:
        _sockobj.connect((_serverHost, _serverPort))   # connect to LV
        isConnected = 1
        return 0
    except _socket.error:
        print "Error connecting. Check if you have the right ip and port. " \
                + "Also check if Labview is running and waiting for the " \
                + "message."
        return 1
        


def disconnect():
    'closes the connection to LabVIEW Server'
    global isConnected
    _sockobj.close()                             # close socket
    isConnected = 0


def _passCommand(command):
    'passes a command to LabVIEW Server'
    _sockobj.send(command)
    data = _sockobj.recv(65536)
    #execString = "lvdata = " + data
    #exec execString
    #return lvdata
    return data


class _Instrument:
    
    def __init__(self, _instrumentName, _functionNames):
        
        for _functionName in _functionNames:
            _execString = "self." + _functionName + " =_Function('" + _instrumentName + "." + _functionName + "')"
            exec _execString


class _Function:
    
    def __init__(self, name):

        self._name = name

    def __call__(self, a = None):

        if isConnected:        
        
            if (a == None):
            
                return _passCommand(self._name + '()')
        
            else:
            
                return _passCommand(self._name + '(' + `a` + ')')

        else: print 'Not Connected: Run "%s.connect()" method to connect.'% __name__