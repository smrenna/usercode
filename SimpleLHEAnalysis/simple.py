import ROOT
import sys,glob


#ROOT.gEnv.SetValue("TFile.Recover",0)
# important!  This doesn't work.  Set in local .rootrc
filename=sys.argv[1]
f = ROOT.TFile(filename, "READ")
dirlist = f.GetListOfKeys()

 
f.cd("demo")

t=ROOT.gDirectory.GetListOfKeys()

c1=ROOT.TCanvas()
c1.SaveAs("test.ps[")
for k in t:
	tp=k.GetName()
	f.cd("demo/"+tp)
	tt=ROOT.gDirectory.GetListOfKeys()
	xmin=0.03
	xmax=0.97
	ymin=0.02
	ymax=0.92
	xstep=(xmax-xmin)/3
	ystep=(ymax-ymin)/3
	padList=[]
	for j in range(0,9):
		ix=j%3
		iy=j/3
		dx=xmin+xstep*ix
		dy=ymin+ystep*iy	
		padList.append(ROOT.TPad(tp,tp,dx,dy,dx+xstep,dy+ystep))
		padList[j].Draw()
		print(dx,dy,dx+xstep,dy+ystep)
	j=0
	print(padList)
	for kk in tt:
		ttp=kk.GetName()
		hnew_=ROOT.TH1F()
		ROOT.gDirectory.GetObject(ttp,hnew_)
		print(j)
		pad_=padList[j]
#		pad_.Draw()
		if j==0:
			label_=ROOT.TPaveLabel(0.3,0.94,0.7,0.98,tp)
			label_.Draw()
		pad_.cd()
		hnew_.DrawCopy()
#		ttext_=ROOT.TText()
#		ttext_.DrawTextNDC(0.5,0.95,tp)
#		pad_.Close()
		j=j+1
	c1.SaveAs("test.ps")
	print(padList)
	padList[8].Close()
	padList[7].Close()
	padList[6].Close()
	padList[5].Close()
	padList[4].Close()
	padList[3].Close()
	padList[2].Close()
	padList[1].Close()
	padList[0].Close()	
#	for j in range(0,6):
#		pad_=padList[j]
#		pad_.Clear()
	f.cd("demo")

c1.SaveAs("test.ps]")
sys.exit(0)

h1 = ROOT.TH1F()
tp = "higgs_pT [#1]"
#higgs_mass and higgs_rap
ROOT.gDirectory.GetObject(tp,h1)
#f.Close()

filename="H_WW_M.root"
g = ROOT.TFile(filename, "READ")
g.cd("jetsPt")
h2 = ROOT.TH1F()
tp = "higgs_pT [#1]"
#higgs_mass and higgs_rap
ROOT.gDirectory.GetObject(tp,h2)
#g.Close()

filename="H_WW_L.root"
x = ROOT.TFile(filename, "READ")
x.cd("jetsPt")
h3 = ROOT.TH1F()
tp = "higgs_pT [#1]"
#higgs_mass and higgs_rap
ROOT.gDirectory.GetObject(tp,h3)
#x.Close()

h1.SetLineColor(1)
h2.SetLineColor(2)
h3.SetLineColor(3)

myPlot=ROOT.TCanvas("myPlot","Histo comparison",0,0,500,700)
pad1=ROOT.TPad("pad1","pad1",0,0.3,1,1)
pad2=ROOT.TPad("pad2","pad2",0,0,1,0.3)
#pad2=ROOT.TPad("pad2","pad2",0,0,1,1)

pad1.Draw()
pad2.Draw()
pad1.cd()
h3.DrawCopy("")
h2.DrawCopy("same")
h1.DrawCopy("same")

pad2.cd()

h3.Divide(h1)
h2.Divide(h1)
h3.DrawCopy("")
h2.DrawCopy("same")


myPlot.SaveAs("pTHiggs.png")
