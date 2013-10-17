import os,sys,glob, re

#def toNumber(streeng):
#  try:
#    return int(streeng)
#  except ValueError:
#    pass
#  return float(streeng)
#
def checkSlha(slhaFileName):
  splitFileName = slhaFileName.split("/")
  slhaFile = open(slhaFileName, 'r')
  
  decayLines = []
  massBlockLines = []
  inMassBlock = False
  
  massFlag = True
  widthFlag = True
  
  for line in slhaFile:
	
    if line[:5] == 'DECAY':
      decayLines.append(line)
        
    if inMassBlock:
      if line[:1] == '#':
        inMassBlock = False
        continue
      massBlockLines.append(line)
        
    if line[:25] == '# PDG code           mass':
      inMassBlock = True
    
  for line in massBlockLines:
    numbers = re.findall('[0-9.\-+E]{1,16}', line)
    if float(numbers[1]) < 0 and (float(numbers[0]) != 1000025):
      massFlag = False
      break
          
  for line in decayLines: 
    numbers = re.findall('[0-9.\-+E]{1,16}', line)
    if (float(numbers[2]) == 0.0) and (int(numbers[1]) != 1000022):
      widthFlag = False
    

  if widthFlag == False:
    print "# Other stable SUSY particle which isn't chi_10\n" 
    print "# Throwing out: " + splitFileName[-1]+ "\n"
    
  if massFlag == False:
    print "# Particle with negative mass which isn't chi_30\n"
    print "# Throwing out: " + splitFileName[-1]+ "\n"
  return (massFlag and widthFlag)


#---Main Execution Point---#D50000#FFFF80---------------------------------------
#	jobno=toNumber(sys.argv[1])

if __name__ == '__main__':
  
  offset = int(sys.argv[1])
  jobsize = int(sys.argv[2])
  newdir=sys.argv[3]
  m0_min=offset
  m0_max=offset + jobsize
  m0_step=20
  m1_min=20
  m1_max=1000
  m1_step=20
  m0_range = (m0_max-m0_min)/m0_step+1
  m1_range = (m1_max-m1_min)/m1_step+1
  scan_range = m0_range*m1_range
  print(scan_range)
  # don't clobber this directory
  #	newdir="/uscms_data/d2/mrenna/devel/CMSSW_4_2_3/src/UserCode/SusyAnalysis/SLHAFILES/mSugraScan/m0_m12_40_m500_1"
  newdir=sys.argv[3]
  

  for jobno in range(0,scan_range):
    m0_x = jobno/m1_range
    m1_x = jobno % m1_range
    
    m0= m0_min + m0_step*m0_x
    m1= m1_min + m1_step*m1_x

    newname=str("msugra_"+str(m0)+"_"+str(m1)+"_40_m500_1.slha")
    print "----------------------------"
    print "mSugra point: m0=" + str(m0)+ ", m12=" +str(m1)
    print "----------------------------"
    os.system("cp lesHouchesInput lesHouchesInput.bak")
    os.system("sed -i -e s,M0INPUT,"+str(m0)+", lesHouchesInput")
    os.system("sed -i -e s,M1INPUT,"+str(m1)+", lesHouchesInput")
    os.system("./softpoint.x leshouches < lesHouchesInput > slhaspectrum.in")
    os.system("mv lesHouchesInput.bak lesHouchesInput")
    f=open("slhaspectrum.in")
    x=f.readlines()
    f.close()
    print(x[-1])
    if x[-1].find("problem with point")>-1:
      print "# Throwing out " + newname
      continue
    os.system("./run")
    os.system("mv susyhit_slha.out "+newdir+"/"+newname)
    if checkSlha(newdir+"/"+newname) == False:      
      os.system("rm " + newdir + "/" +newname)


