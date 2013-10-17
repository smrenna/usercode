import os,sys,glob

def toNumber(streeng):
  try:
    return int(streeng)
  except ValueError:
    pass
  return float(streeng)

#---Main Execution Point---#D50000#FFFF80---------------------------------------
#	jobno=toNumber(sys.argv[1])

if __name__ == '__main__':

	m0_min=20
	m0_max=2000
	m0_step=20
	m1_min=20
	m1_max=760
	m1_step=20
	m0_range = (m0_max-m0_min)/m0_step+1
	m1_range = (m1_max-m1_min)/m1_step+1
	scan_range = m0_range*m1_range
	print(scan_range)


	for jobno in range(0,scan_range):


		m0_x = jobno/m1_range
		m1_x = jobno % m1_range

		m0= m0_min + m0_step*m0_x
		m1= m1_min + m1_step*m1_x

		newname=str("msugra_"+str(m0)+"_"+str(m1)+"_10_m500_1.slha")
		newdir="/uscms_data/d2/mrenna/devel/CMSSW_4_2_3/src/UserCode/SusyAnalysis/SLHAFILES/mSugraScan/m0_m12_10_m500_1"
		print(m0,m1)
		os.system("cp lesHouchesInput lesHouchesInput.bak")
		os.system("sed -i -e s,M0INPUT,"+str(m0)+", lesHouchesInput")
		os.system("sed -i -e s,M1INPUT,"+str(m1)+", lesHouchesInput")
		os.system("./softpoint.x leshouches < lesHouchesInput > slhaspectrum.in")
		os.system("mv lesHouchesInput.bak lesHouchesInput")
		f=open("slhaspectrum.in")
		x=f.readlines()
		f.close()
		print(x[-1])
		if x[-1].find("problem with point")>-1: continue
		os.system("./run")
		os.system("mv susyhit_slha.out "+newdir+"/"+newname)
	

