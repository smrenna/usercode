import os,sys,glob

os.system("touch 5step.lep")
g = open('5step.lhe','a')

for l in glob.glob("/pnfs/cms/WAX/resilient/kristian/darkstuff/LHE_5step/*.lhe"):
	os.system("dccp "+l+" .")
	temp=l.split("/")
	file=temp[-1]

	f = open(file,'r')

	line = f.readline().strip()

	while line:


		if line.find("<event>")>-1:
			line = f.readline().strip()
			line = f.readline().strip()
			line = f.readline().strip()
			line = f.readline().strip()
			line = f.readline().strip()
			line = f.readline().strip()
			g.write(line+"\n")
		

		line = f.readline().strip()


	f.close()
        os.system("rm "+file)
g.close()

	

	
