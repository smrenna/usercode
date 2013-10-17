import ROOT
import sys,glob


#ROOT.gEnv.SetValue("TFile.Recover",0)
# important!  This doesn't work.  Set in local .rootrc

files=glob.glob("test*.root")
files.sort()

#for filename in glob.glob("TN_*.root"):
for filename in files:

	f = ROOT.TFile(filename, "READ")
	
	if f.IsZombie(): continue
		
	dirlist = f.GetListOfKeys()
        for k in dirlist:
		print k.GetName()

        print(dirlist)
	f.cd("plotMHT")

	t=ROOT.gDirectory.GetListOfKeys()

	for k in t:
		tp=k.GetName()
		if tp.find("MHT")>-1:
			hnew_=ROOT.TH1F()
			ROOT.gDirectory.GetObject(tp,hnew_)
			print filename,hnew_.Integral()/10000.0


	f.Close()
