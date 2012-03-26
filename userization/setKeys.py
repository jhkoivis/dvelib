
import subprocess
import os

def checkUbuntu():

	a = subprocess.Popen(	"uname --all", 
				shell = True, 
				stdout = subprocess.PIPE)

	for line in a.stdout:
		if line.find('buntu') >= 0:
			return 1

	return 0

def addKeybindings():
	lines = ['<?xml version="1.0"?>']
	lines.append('<gconf>')
	lines.append('<entry name="panel_run_dialog" mtime="1308671339" type="string">')
	lines.append('<stringvalue>&lt;Mod4&gt;f</stringvalue>')
        lines.append('</entry>')
	lines.append('<entry name="run_command_terminal" mtime="1308672232" type="string">')
        lines.append('<stringvalue>&lt;Mod4&gt;t</stringvalue>')
        lines.append('</entry>')
	lines.append('</gconf>')

	fn = os.path.expanduser('~/.gconf/apps/metacity/global_keybindings/%gconf.xml')
	outfile = open(fn, 'w')
	for item in lines:
		outfile.write(item + '\n')
	
	outfile.close()


if checkUbuntu():
	print "Ubuntu found"
	print "adding keybindings...",
	addKeybindings()
	print "done"





