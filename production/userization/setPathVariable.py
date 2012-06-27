
import subprocess

class SetPathVariable:
    
    def winGetOldPath(self):
        cmd = 'reg.exe QUERY '
        cmd+= ' "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" '
        cmd+= ' /v PATH '
        a = subprocess.Popen(cmd, shell = True,
                             stdout = subprocess.PIPE)
        path = a.stdout.readlines()[-2].strip()[4:].strip()[13:].strip()
        self.winSaveOldPath(path)
        return path
    
    def winSaveOldPath(self, pathStr):
        f = open('./path.log','a')
        f.write('\n' + pathStr)
        f.close()
        
    def winSetNewPath(self, path):
        cmd = 'reg.exe ADD '
        cmd+= ' "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" '
        cmd+= ' /v Path /t REG_EXPAND_SZ /d "%s" /f' % (path)
        #reg.exe ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d %newPath% /f
        print cmd
        a = subprocess.Popen(cmd, shell = True,
                             stdout = subprocess.PIPE)
        #print a.stdout.readlines()
    
    def winAppendPath(self, path):
        print 'appending path:', path
        oldPath = self.winGetOldPath()
        if oldPath.find(';' + path) > 0: 
            print 'path exists, nothing done.'
            return
        newPath = oldPath + ';' + path
        self.winSetNewPath(newPath)
        print 'path appended'
        
        
        