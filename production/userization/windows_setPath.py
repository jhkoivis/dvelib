
from glob import glob
import subprocess
import os 
from programHandler import ProgramHandler


# get program path
environmetVars = os.environ.keys()
programLocs = []
#if environmentVars.__contains__('PROGRAMW6432'):
for dir in 'PROGRAMW6432', 'HOMEDRIVE', 'SYSTEMDRIVE', 'PROGRAMFILES', 'PROGRAMFILES(86)': 
    try:
        programLocs.append(os.environ[dir])
    except:
        pass
print programLocs

ph = ProgramHandler()
for dir in programLocs:
    for pdir in glob(dir + '/*'):
        ph.handleFlagged(pdir)

