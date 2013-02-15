

import subprocess

p = subprocess.Popen(	'svn up', 
			cwd = '/var/www', 
			shell = True)


