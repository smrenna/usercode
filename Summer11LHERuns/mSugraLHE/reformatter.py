import math,sys,re,os,shutil
from xml.dom import minidom

import fileinput


#main part of analysis
if len(sys.argv)!=3:
    print "Usage: reformatter.py <infile> model_description    "
    print "     : input file is backed up but overwritten "
    print " Last modified: Wed Apr  6 14:08:27 CDT 2011 "

    sys.exit(0)
else:
    print "Running reformatter.py to reformat Pythia LHE file"

file = sys.argv[1]

modelname = sys.argv[2]

#let xml find the event tags
try:
    xmldoc = minidom.parse(sys.argv[1])
except IOError:
    print " could not open file for xml parsing ",sys.argv[1]
    sys.exit(0)

shutil.copyfile(file,file+".bak")


reflist = xmldoc.firstChild


for ref in reflist.childNodes:
	if ref.nodeName=='header':
		ref.appendChild(x)
	if ref.nodeName=='event':
		ref.firstChild.appendData("# model "+modelname+"\n")

t=xmldoc.toprettyxml(indent="",newl="")
f=open(file,'w')
f.write(t)
f.close()

f=open(file,'r')
o=open(file+".tmp",'w')

for i, line in enumerate(f):
	if line.find("-->")>-1:
		o.write(line)
		o.write('<header>\n')
		o.write('<slha>\n')
		o.write("DECAY   1000022   0.0E+00\n")
		o.write('</slha>\n')				
		o.write('</header>\n')
	else:
		o.write(line)

f.close()
o.close()
os.remove(file)
os.rename(file+".tmp", file)


