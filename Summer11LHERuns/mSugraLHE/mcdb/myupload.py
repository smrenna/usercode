import os,sys,glob,popen2
from subprocess import *

artid=sys.argv[1]
if len(sys.argv)<2:
	sys.exit(0)

for file in glob.glob("msugra*.lhe"):
        r,w=popen2.popen2("grep \<event "+file+" | wc --lines")
        pipe=r.readline()
        r.close()
        w.close()
	print(file,int(pipe))
 	os.system("perl upload2mcdb.pl -artid "+artid+" -uploadonly "+file)	
