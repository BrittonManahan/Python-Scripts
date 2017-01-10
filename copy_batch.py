from winappdbg import Debug
from winappdbg.win32 import *
import winappdbg
import sys
import re
from shutil import copyfile
import ntpath

# Debugger Event Handler
class MyEventHandler( winappdbg.EventHandler ):
	
	# Here we set which API calls we want to intercept.
	apiHooks = {
        # Hooks for the kernel32 library.
        'kernel32.dll' : [
		# Hook for CreateProcessW
			( 'CreateProcessW'  , (PVOID, PVOID, PVOID, PVOID, DWORD, DWORD, PVOID, PVOID, PVOID, PVOID) ), 
        ],
    }
	
	def pre_CreateProcessW(self, event, ra, lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes, bInheritHandles, dwCreationFlags, lpEnvironment, lpCurrentDirectory, lpStartupInfo, lpProcessInformation):
		proc = event.get_process()
		string = format(ra, '#010x')
		print  "%s: CreateProcessW" % (string)
		string = proc.peek_string( lpApplicationName, fUnicode = True )
		print "\t lpApplicationName: %s" % string
		string = proc.peek_string( lpCommandLine, fUnicode = True )
		print "\t lpCommandLine: %s" % string
		print "\t dwCreationFlags: %d" % dwCreationFlags
		files = re.findall(r"C:\\[^.]+\.{1}[\w]+", string)
		for file in files:
			if "bat" in file:
				print "Saving copy of batch file!"
				destfile = "C:\\log\\files\\" + ntpath.basename(file)
				print "%s --> %s" % (file,destfile)
				copyfile(file, destfile)		
			
### F.2
# simple_debugger(argv):
###
def simple_debugger(filename):
  #global logfile

  try:
    handler = MyEventHandler()
  except:
    traceback.print_exc()
  with winappdbg.Debug(handler,bKillOnExit = True) as debug:
  
	print "[*] Starting %s" % filename
	
	debug.execl(filename)
		
	print "[*] Starting debug loop"

	debug.loop()
	
	print "[*] Terminating"

simple_debugger(sys.argv[1])