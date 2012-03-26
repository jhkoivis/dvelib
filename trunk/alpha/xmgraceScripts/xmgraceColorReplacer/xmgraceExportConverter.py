

"""
this program loads gracefile to a dict
"""

import numpy

def readCommand(strippedLine):
    """
        return a dictionary from line
    """
    splitted = strippedLine.split()
    if not splitted[0].strip()[0] == '@':
        raise TypeError('not a command: %s' % (strippedLine))
    
    test = splitted[0].strip()
    if len(test) > 1:
        splitted2 = ['@']
        splitted2.append(splitted[0][1:])
        splitted2 += splitted[1:]
        splitted = splitted2
    
    cmd = {} 
    cmd['name'] = splitted[1].strip()
    cmd['content'] = {}
    #print cmd['name']

    contentNo = 0
    for item in splitted[2:]:
        cmd['content']['%02d' % (contentNo)] = item.strip() 
        contentNo += 1
        
    return cmd


inFile = open('data.agr')

allCommands = []
dataSets = {}

cmd = {}
for line in inFile:
    if line.strip()[0] == '#': continue
    if line.strip()[0] == '&': continue
    
    # if last command was 'with' it affects the following
    if line.strip()[0] == '@' and line.strip()[1].isspace():
        if cmd.has_key('name') and cmd.has_key('content') and cmd['content'].has_key('00'):
            if cmd['name'] == 'with':
                stripped = '@with '
                stripped += cmd['content']['00'] + ' '
                line2 = line.strip()[1:]
                stripped += line2
            else:
                stripped = line.strip()
        else:
            stripped = line.strip()
    else:
        stripped = line.strip()
    
    
    if stripped[0] == '@': # we have commands
        cmd = readCommand(stripped)
        allCommands.append(cmd)
    
    else: # we have data
        if not len(allCommands) >= 2:
            raise TypeError('not a valid xmgrace file')
        prevCmd = allCommands[-1]
        prevPrevCmd = allCommands[-2]
        setName = None
        if prevPrevCmd.has_key('name'):
            if prevPrevCmd['name'] == 'target': 
                if cmd.has_key('content'):
                    setName = prevPrevCmd['content']['00']
        if not dataSets.has_key(setName):
            dataSets[setName] = []
        splitted = line.split()
        stripped = map(lambda x: x.strip(), splitted)
        floated = map(float, splitted)
        dataSets[setName].append(floated)
        
#print dataSets
for key in dataSets.keys():
    fileName = key
    #outFile = open(fileName + '.dat', 'w')
    data = numpy.array(dataSets[key])
    try:
        numpy.savetxt(fileName + '.data', data)
    except:
        print data
        raise
        
        
        