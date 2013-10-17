import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak5GenJets_cfi import *

genWBoson = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" abs(pdgId)==24 && (status==3 || status==62) ")
)

plotGenWBoson= cms.EDAnalyzer(
	"CandViewHistoAnalyzer",
	src = cms.InputTag("genWBoson"),							   
	histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(300.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("W_pT_logscale"),
	    description = cms.untracked.string("W_pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(50.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("W_pT_low"),
	    description = cms.untracked.string("W_pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),		
	    cms.PSet(
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("W_rapidity"),
	    description = cms.untracked.string("W_rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(-3.2),
	    max = cms.untracked.double(3.2),
	    nbins = cms.untracked.int32(32),
	    name = cms.untracked.string("W_phi"),
	    description = cms.untracked.string("W_#varphi"),
	    plotquantity = cms.untracked.string("phi")
	    ),		
		)
)


genLeptons = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" ( abs(pdgId)==11 || abs(pdgId)==13 ) && status==1 && ( abs(mother(0).pdgId)==24  || abs(mother(0).pdgId)==11 || abs(mother(0).pdgId)==13 ) ")
)

myGenParticlesForJets = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticlesForJetsNoNu"),
#  cut = cms.string("pt>-1")
  cut = cms.string(" !(( abs(pdgId)==11 || abs(pdgId)==13 ) && status==1 && ( abs(mother(0).pdgId)==24  || abs(mother(0).pdgId)==11 || abs(mother(0).pdgId)==13 ) )")
)

ak5GenJets.src = cms.InputTag("myGenParticlesForJets")


genNeutrinos = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" ( abs(pdgId)==12 || abs(pdgId)==14 ) && status==1 && ( abs(mother(0).pdgId)==24  || abs(mother(0).pdgId)==12 || abs(mother(0).pdgId)==14 ) ")
)


WCand = cms.EDProducer("CandViewShallowCloneCombiner",
     decay = cms.string("genLeptons genNeutrinos"),
     checkCharge = cms.bool(False),
	 cut = cms.string(" pt>-1 ")
)

# merge leptons and neutrino into W candidates
##WCand = cms.EDProducer("CandMerger",
##   src = cms.VInputTag("genLeptons", "genNeutrinos")
##)

##transverseW = cms.EDProducer("CompositeProducer",
##   dauSrc = cms.InputTag("WCand")
##)

transverseW = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("WCand"),
  cut = cms.string(" pt>-1 ")
)

plotTransverseW= cms.EDAnalyzer(
	"CandViewHistoAnalyzer",
	src = cms.InputTag("transverseW"),							   
	histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(150.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("transW_pT_logscale"),
	    description = cms.untracked.string("W_pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(150.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("transW_mass"),
	    description = cms.untracked.string("W_mT [GeV/c]"),
	    plotquantity = cms.untracked.string("sqrt(2*daughter(0).pt*daughter(1).pt*(1.0-cos(daughter(0).phi - daughter(1).phi) ) )")
	   )
   )
)



printGenLeptons = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(10)
)

printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genLeptons"),
     maxEventsToPrint = cms.untracked.int32(10)
)


highestPtJet = cms.EDFilter("LargestPtCandViewSelector",
	 src = cms.InputTag("ak5GenJets"),
	 maxNumber = cms.uint32(1)
)

printHighest = cms.EDAnalyzer("ParticleListDrawer",
#     src = cms.InputTag("highestPtJet"),
     src = cms.InputTag("transverseW"),
     maxEventsToPrint = cms.untracked.int32(10)
)


leptonPlusJet = cms.EDProducer("CandViewShallowCloneCombiner",
     decay = cms.string("genLeptons highestPtJet"),
     checkCharge = cms.bool(False),
	 cut = cms.string(" pt>-1 ")
)

plotLeptonPlusJet= cms.EDAnalyzer(
	"CandViewHistoAnalyzer",
	src = cms.InputTag("leptonPlusJet"),							   
	histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(10.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("lepton-Jet_dEta"),
	    description = cms.untracked.string("#Delta#eta(l,j1)"),
	    plotquantity = cms.untracked.string("abs(daughter(0).eta - daughter(1).eta)")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(-3.2),
	    max = cms.untracked.double(3.2),
	    nbins = cms.untracked.int32(64),
	    name = cms.untracked.string("lepton-Jet_dPhi"),
	    description = cms.untracked.string("#Delta#varphi(l,j1)"),
	    plotquantity = cms.untracked.string("deltaPhi(daughter(0).phi,daughter(1).phi)")
	    ),		
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(6.2),
	    nbins = cms.untracked.int32(64),
	    name = cms.untracked.string("lepton-Jet_dR"),
	    description = cms.untracked.string("#Delta R(l,j1)"),
	    plotquantity = cms.untracked.string("deltaR(daughter(0).eta,daughter(0).phi,daughter(1).eta,daughter(1).phi)")
	    )		
		)
)


# should require e/mu to be isolated
selectedJets = cms.EDFilter("CandViewShallowCloneProducer",
    src = cms.InputTag("ak5GenJets"),
    cut = cms.string("pt > 25 & abs( eta ) < 2.5")
)


plotGenLeptons= cms.EDAnalyzer("CandViewHistoAnalyzer",
				src = cms.InputTag("genLeptons"),							   
 histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(150.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("lep_pT_logscale"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(60.0),
	    nbins = cms.untracked.int32(60),
	    name = cms.untracked.string("lep_pT_low"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),		
	    cms.PSet(
	    min = cms.untracked.double(60.0),
	    max = cms.untracked.double(120.0),
	    nbins = cms.untracked.int32(60),
	    name = cms.untracked.string("lep_pT_hi"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),		
	    cms.PSet(
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("lep_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)




plotGenJets= cms.EDAnalyzer("CandViewHistoAnalyzer",
#				src = cms.InputTag("ak5GenJets"),							   
				src = cms.InputTag("selectedJets"),							   
 histograms = cms.VPSet(
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(3),
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(150.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("jet_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
		cms.PSet(
            itemsToPlot = cms.untracked.int32(3),
		min = cms.untracked.double(0.0),
	    max = cms.untracked.double(25.0),
	    nbins = cms.untracked.int32(25),
	    name = cms.untracked.string("jet_mass"),
	    description = cms.untracked.string("mass [GeV/c^2]"),
	    plotquantity = cms.untracked.string("mass")
	    ),
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(3),
	    min = cms.untracked.double(-3.0),
	    max = cms.untracked.double(3.0),
	    nbins = cms.untracked.int32(20),
	    name = cms.untracked.string("jet_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)

chargedTracks = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("myGenParticlesForJets"),
  cut = cms.string(" charge!= 0 && pt>0.1 ")
)

plotChargedTracks= cms.EDAnalyzer("CandViewHistoAnalyzer",
				src = cms.InputTag("chargedTracks"),
 histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(100.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("cc_pT_logscale"),
	    description = cms.untracked.string("cc_pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("cc_pT_low"),
	    description = cms.untracked.string("cc_pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),		
	    cms.PSet(
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("cc_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)

transverseWPlusCC = cms.EDProducer("CandViewShallowCloneCombiner",
     decay = cms.string("transverseW chargedTracks"),
     checkCharge = cms.bool(False),
	 cut = cms.string(" pt>-1 ")
)

plotWPlusCC= cms.EDAnalyzer(
	"CandViewHistoAnalyzer",
	src = cms.InputTag("transverseWPlusCC"),							   
	histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(-3.2),
	    max = cms.untracked.double(3.2),
	    nbins = cms.untracked.int32(64),
	    name = cms.untracked.string("W-CC_dPhi"),
	    description = cms.untracked.string("#Delta#varphi(W,cc)"),
	    plotquantity = cms.untracked.string("deltaPhi(daughter(0).phi,daughter(1).phi)")
	    ),		
		)
)





analysis = cms.Sequence(
	myGenParticlesForJets*
	ak5GenJets*
        selectedJets*
	genWBoson *
	plotGenWBoson *
	genLeptons*
	plotGenLeptons*
	genNeutrinos*
	highestPtJet*
        WCand*
        transverseW*
 	printGenParticles*
 	printGenLeptons*
	printHighest*
        plotTransverseW*
        leptonPlusJet*
        plotLeptonPlusJet*
    plotGenJets*
	chargedTracks*
	plotChargedTracks 
#	transverseWPlusCC*
#	plotWPlusCC

						 )


