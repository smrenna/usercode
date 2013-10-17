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
        m12a=float(sa[3])
        m12b=float(sb[3])
        if m0a!=m0b: return cmp(m0a,m0b)
        return cmp(m12a,m12b)

def mysort2(aa,bb):
        a=aa.replace(".lhe","")
        b=bb.replace(".lhe","")
        a=a.split("/")[-1]
        b=b.split("/")[-1]        
        sa=a.split("_")
        sb=b.split("_")
        m0a=float(sa[2])
        m0b=float(sb[2])
        m12a=float(sa[3])
        m12b=float(sb[3])
        if m0a!=m0b: return cmp(m0a,m0b)
        return cmp(m12a,m12b)

header=str("<LesHouchesEvents>\n\
<!--\n\
File generated with PYTHIA 6.424\n\
-->\n\
<header>\n\
<MGVersion>\n\
# MG/ME version    : 4.0.0\n\
</MGVersion>\n\
<MGProcCard>\n\
# Begin PROCESS # This is TAG. Do not modify this line\n\
pp>MODELTAG    @0       # First Process\n\
# End PROCESS  # This is TAG. Do not modify this line\n\
</MGProcCard>\n\
<MGGenerationInfo>\n\
#  Number of Events        :      NUMEVT\n\
</MGGenerationInfo>\n\
<slha>\n\
DECAY   1000022   0.0E+00\n\
</slha>\n\
</header>\n\
<init>\n\
    2212    2212  3.500000E+03  3.500000E+03     0     0 10042 10042     3    84\n\
  1.000000E+00  1.000000E+00  1.000000E+00   201\n\
  1.000000E+00  1.000000E+00  1.000000E+00   202\n\
  1.000000E+00  1.000000E+00  1.000000E+00   204\n\
  1.000000E+00  1.000000E+00  1.000000E+00   205\n\
  1.000000E+00  1.000000E+00  1.000000E+00   207\n\
  1.000000E+00  1.000000E+00  1.000000E+00   208\n\
  1.000000E+00  1.000000E+00  1.000000E+00   209\n\
  1.000000E+00  1.000000E+00  1.000000E+00   210\n\
  1.000000E+00  1.000000E+00  1.000000E+00   211\n\
  1.000000E+00  1.000000E+00  1.000000E+00   212\n\
  1.000000E+00  1.000000E+00  1.000000E+00   213\n\
  1.000000E+00  1.000000E+00  1.000000E+00   214\n\
  1.000000E+00  1.000000E+00  1.000000E+00   216\n\
  1.000000E+00  1.000000E+00  1.000000E+00   217\n\
  1.000000E+00  1.000000E+00  1.000000E+00   218\n\
  1.000000E+00  1.000000E+00  1.000000E+00   219\n\
  1.000000E+00  1.000000E+00  1.000000E+00   220\n\
  1.000000E+00  1.000000E+00  1.000000E+00   221\n\
  1.000000E+00  1.000000E+00  1.000000E+00   222\n\
  1.000000E+00  1.000000E+00  1.000000E+00   223\n\
  1.000000E+00  1.000000E+00  1.000000E+00   224\n\
  1.000000E+00  1.000000E+00  1.000000E+00   225\n\
  1.000000E+00  1.000000E+00  1.000000E+00   226\n\
  1.000000E+00  1.000000E+00  1.000000E+00   227\n\
  1.000000E+00  1.000000E+00  1.000000E+00   228\n\
  1.000000E+00  1.000000E+00  1.000000E+00   229\n\
  1.000000E+00  1.000000E+00  1.000000E+00   230\n\
  1.000000E+00  1.000000E+00  1.000000E+00   231\n\
  1.000000E+00  1.000000E+00  1.000000E+00   232\n\
  1.000000E+00  1.000000E+00  1.000000E+00   233\n\
  1.000000E+00  1.000000E+00  1.000000E+00   234\n\
  1.000000E+00  1.000000E+00  1.000000E+00   235\n\
  1.000000E+00  1.000000E+00  1.000000E+00   236\n\
  1.000000E+00  1.000000E+00  1.000000E+00   237\n\
  1.000000E+00  1.000000E+00  1.000000E+00   238\n\
  1.000000E+00  1.000000E+00  1.000000E+00   239\n\
  1.000000E+00  1.000000E+00  1.000000E+00   240\n\
  1.000000E+00  1.000000E+00  1.000000E+00   241\n\
  1.000000E+00  1.000000E+00  1.000000E+00   242\n\
  1.000000E+00  1.000000E+00  1.000000E+00   243\n\
  1.000000E+00  1.000000E+00  1.000000E+00   244\n\
  1.000000E+00  1.000000E+00  1.000000E+00   246\n\
  1.000000E+00  1.000000E+00  1.000000E+00   247\n\
  1.000000E+00  1.000000E+00  1.000000E+00   248\n\
  1.000000E+00  1.000000E+00  1.000000E+00   249\n\
  1.000000E+00  1.000000E+00  1.000000E+00   250\n\
  1.000000E+00  1.000000E+00  1.000000E+00   251\n\
  1.000000E+00  1.000000E+00  1.000000E+00   252\n\
  1.000000E+00  1.000000E+00  1.000000E+00   253\n\
  1.000000E+00  1.000000E+00  1.000000E+00   254\n\
  1.000000E+00  1.000000E+00  1.000000E+00   256\n\
  1.000000E+00  1.000000E+00  1.000000E+00   258\n\
  1.000000E+00  1.000000E+00  1.000000E+00   259\n\
  1.000000E+00  1.000000E+00  1.000000E+00   261\n\
  1.000000E+00  1.000000E+00  1.000000E+00   262\n\
  1.000000E+00  1.000000E+00  1.000000E+00   263\n\
  1.000000E+00  1.000000E+00  1.000000E+00   264\n\
  1.000000E+00  1.000000E+00  1.000000E+00   265\n\
  1.000000E+00  1.000000E+00  1.000000E+00   271\n\
  1.000000E+00  1.000000E+00  1.000000E+00   272\n\
  1.000000E+00  1.000000E+00  1.000000E+00   273\n\
  1.000000E+00  1.000000E+00  1.000000E+00   274\n\
  1.000000E+00  1.000000E+00  1.000000E+00   275\n\
  1.000000E+00  1.000000E+00  1.000000E+00   276\n\
  1.000000E+00  1.000000E+00  1.000000E+00   277\n\
  1.000000E+00  1.000000E+00  1.000000E+00   278\n\
  1.000000E+00  1.000000E+00  1.000000E+00   279\n\
  1.000000E+00  1.000000E+00  1.000000E+00   280\n\
  1.000000E+00  1.000000E+00  1.000000E+00   281\n\
  1.000000E+00  1.000000E+00  1.000000E+00   282\n\
  1.000000E+00  1.000000E+00  1.000000E+00   283\n\
  1.000000E+00  1.000000E+00  1.000000E+00   284\n\
  1.000000E+00  1.000000E+00  1.000000E+00   285\n\
  1.000000E+00  1.000000E+00  1.000000E+00   286\n\
  1.000000E+00  1.000000E+00  1.000000E+00   287\n\
  1.000000E+00  1.000000E+00  1.000000E+00   288\n\
  1.000000E+00  1.000000E+00  1.000000E+00   289\n\
  1.000000E+00  1.000000E+00  1.000000E+00   290\n\
  1.000000E+00  1.000000E+00  1.000000E+00   291\n\
  1.000000E+00  1.000000E+00  1.000000E+00   292\n\
  1.000000E+00  1.000000E+00  1.000000E+00   293\n\
  1.000000E+00  1.000000E+00  1.000000E+00   294\n\
  1.000000E+00  1.000000E+00  1.000000E+00   295\n\
  1.000000E+00  1.000000E+00  1.000000E+00   296\n\
</init>\n")



#main part of analysis
if len(sys.argv)<4:
	print "Usage: mcdb_many.py <directory> <job number> <max file shower in GB> <model stub>"
	print "     : input file is backed up but overwritten "
	print "     : Where file_list.txt is a file with one filename (MUST end in .lhe)."
	print " Last modified: Wed Apr  6 14:08:27 CDT 2011 "

	sys.exit(0)
else:
    print "Running mcdb_many.py to reformat Pythia LHE file"


pnfs_directory = sys.argv[1]
model_stub = sys.argv[4]

search_path = str("/").join([pnfs_directory,model_stub])

filelist = glob.glob(search_path+'*.tar.gz')
filelist.sort(mysort)

test=len(filelist)
jobno=int(sys.argv[2])
if jobno>test:
   print(" jobno = ",jobno," files = ",test)
   sys.exit(0)

filename = filelist[jobno]

#filenameEnd = str("_").join([temps[-3],temps[-2],temps[-1]])
filenameEnd = ""

tagName = model_stub

header=header.replace("MODELTAG",tagName)

tarfile = "temp.tar.gz"

if filename.find("pnfs")>-1:
   cmd="dc_dccp"
else:
   cmd="cp"
   
subprocess.call([cmd,filename,tarfile])

p=subprocess.Popen("tar tzf "+tarfile,shell=True,stdout=subprocess.PIPE)

component_test=p.stdout.readline().strip()

p.wait()

scomp = len(component_test.split("/"))-1



last_command="--strip-components="+str(scomp)

print(last_command)

subprocess.call(["tar","xzf",tarfile,last_command])

subprocess.call(["rm",tarfile])


filenameBegin = ""
filenameEnd = filenameEnd+str(".lhe")

modellist = glob.glob(model_stub+'*.lhe')
modellist.sort(mysort2)
limit = float(sys.argv[3])

if len(modellist)==0:
   print("no models extracted from file")
   sys.exit(0)

lineNumber = -1

tFilename='temp.lhex'
os.system("rm -f "+tFilename)
os.system("touch "+tFilename)

f = open(tFilename, 'a')
f.writelines(header)

print("modellist",modellist)

runningSize=0
runningEvents=0

for line in modellist:

		
    lineNumber = lineNumber + 1
    file = str(line)

    print(file)

    print(model_stub,file)

    filestrip=file.replace(".lhe","")
    if lineNumber == 0:
       beginFileNumbers = re.findall(model_stub+"_[0-9.]{2,9}_[0-9.]{2,9}", filestrip)

    while file[-3:] != 'lhe':
       file = file[:-1]

    print("started file ",file)
    endFileNumbers = re.findall(model_stub+"_[0-9.]{2,9}_[0-9.]{2,9}", filestrip)

    print("begin",beginFileNumbers)
    print("end",endFileNumbers)


    startWrite="<event"
    endWrite="</LesHouchesEvents>"
    
    ff=open(file,'r')
    statinfo = os.stat(file)
    runningSize = runningSize + statinfo.st_size

#    xbuffer=list()
    writeline=""

    beginWrite = -1

    for thisline in ff:
        if len(thisline)<1: break
        writeline=thisline            
        if beginWrite<0:
          check=thisline.find(startWrite)
          if check>-1: beginWrite=1
#          if startWrite==startWrite0: writeline=startWrite0+">\n"

        if beginWrite<0: continue  

        check=thisline.find(endWrite)
        if check>-1: break
#        xbuffer=xbuffer+writeline
#        xbuffer.append(writeline)
        if writeline.find("<event>")>-1: runningEvents = runningEvents + 1 
        f.write(writeline)
#        print(buffer)

    ff.close()
    os.system("rm "+file)
    print("added ",file)


# count number of events and output    
    if runningSize > (limit*1000000000) or line==modellist[-1]:
      f.write("</LesHouchesEvents>\n")
      f.close()

      fullFileName = (filenameBegin + beginFileNumbers[0] + 'to' +
					endFileNumbers[0][len(model_stub)+1:] + filenameEnd)
      subprocess.call(['mv', filenameBegin + 'temp.lhex', fullFileName])

      subprocess.call(['sed','-i','1,20s/NUMEVT/'+str(runningEvents)+'/',fullFileName])

      print "File size has reached limit. Wrote " + fullFileName
      print "Creating new file..."

      if line!=modellist[-1]:
          beginFileNumbers = re.findall(model_stub+"_[0-9.]{2,9}_[0-9.]{2,9}", file)
          tFilename=filenameBegin + 'temp.lhex'
          os.system("touch "+tFilename)
          f = open(tFilename, 'a')
          f.writelines(header)
      else:
          break

      lineNumber = -1
      runningSize = 0
      runningEvents = 0
