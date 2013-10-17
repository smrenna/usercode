#!/usr/bin/env python

import math,sys,re,os,shutil, subprocess,glob,string
#from xml.dom import minidom

def mysort(aa,bb):
        a=aa.split("/")[-1]
        b=bb.split("/")[-1]
        sa=a.split("_")
        sb=b.split("_")
        m0a=float(sa[1])
        m0b=float(sb[1])
        m12a=float(sa[2])
        m12b=float(sb[2])
        if m0a!=m0b: return cmp(m0a,m0b)
        return cmp(m12a,m12b)


#main part of analysis
if len(sys.argv)<3:
	print "Usage: reformatter.py <directory> <out filename prefix> <out filename postfix> <max file shower in GB> "
	print "     : input file is backed up but overwritten "
	print "     : Where file_list.txt is a file with one filename (MUST end in .lhe)."
	print " Last modified: Wed Apr  6 14:08:27 CDT 2011 "

	sys.exit(0)
else:
    print "Running reformatter.py to reformat Pythia LHE file"

filelist = glob.glob(sys.argv[1]+'/msugra*.lhe')
#filelist = glob.glob('msugra*.lhe')

filelist.sort(mysort)


filenameBegin = ""
filenameEnd = sys.argv[3]
modellist = filelist
#limit = int(sys.argv[4])
limit = float(sys.argv[4])

totalSize=0.0
for file in filelist:
        statinfo = os.stat(file)        
        totalSize=totalSize+float(statinfo.st_size)

nFiles = len(filelist)
targetSize= limit*1000000000
nRuns=int(totalSize/targetSize)+1
filesPerChunk=int(nFiles/nRuns)

nLeft=int(nFiles-nRuns*filesPerChunk)
if nLeft>0: nRuns=nRuns+1

thisRun=int(sys.argv[2])
print(thisRun,nRuns,filesPerChunk)

iStart=thisRun*filesPerChunk
iEnd=iStart+filesPerChunk
if iEnd>nFiles: iEnd=nFiles+1

if iStart>nFiles:
   print("too many runs")
   sys.exit(0)

print(iStart,iEnd,nFiles)

lineNumber = -1

tFilename=filenameBegin + 'temp.tar'
firstfile = 1

runningSize=0

tarlist=modellist[iStart:iEnd]


for iFile in range(iStart,iEnd):


    line=modellist[iFile]

		
    lineNumber = lineNumber + 1
    file = str(line)

    print(file,lineNumber)

    if lineNumber == 0:
       beginFileNumbers = re.findall("msugra_[0-9]{2,4}_[0-9]{2,4}", file)
       os.system("tar cvf "+tFilename+" -P "+file)
    else:
       print(lineNumber,file)
       os.system("tar rvf "+tFilename+" -P "+file)
		
    endFileNumbers = re.findall("msugra_[0-9]{2,4}_[0-9]{2,4}", file)

    



fullFileName = (filenameBegin + beginFileNumbers[0] + 'to' +
		endFileNumbers[0][7:] + filenameEnd)
subprocess.call(['mv', filenameBegin + 'temp.tar', fullFileName])

print "File size has reached limit. Wrote " + fullFileName
