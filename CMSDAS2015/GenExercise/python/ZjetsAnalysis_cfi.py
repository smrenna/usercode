import FWCore.ParameterSet.Config as cms

#from RecoJets.JetProducers.ak5GenJets_cfi import *

genWBoson = cms.EDFilter("CandViewShallowCloneProducer",
#  src = cms.InputTag(options.product),
  cut = cms.string(" abs(pdgId)==23 && (status==3 || status==62) ")
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
#  src = cms.InputTag(options.product),
  cut = cms.string(" ( abs(pdgId)==11 || abs(pdgId)==13 ) && status==1 && ( abs(mother(0).pdgId)==23  || abs(mother(0).pdgId)==11 || abs(mother(0).pdgId)==13 ) ")
)



WCand = cms.EDProducer("CandViewShallowCloneCombiner",
     decay = cms.string("genLeptons@+ genLeptons@-"),
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



#printGenLeptons = cms.EDAnalyzer("ParticleListDrawer",
#     src = cms.InputTag(options.product),
#     maxEventsToPrint = cms.untracked.int32(10)
#)

printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genLeptons"),
     maxEventsToPrint = cms.untracked.int32(10)
)


printHighest = cms.EDAnalyzer("ParticleListDrawer",
#     src = cms.InputTag("highestPtJet"),
     src = cms.InputTag("transverseW"),
     maxEventsToPrint = cms.untracked.int32(10)
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




analysis = cms.Sequence(
	genWBoson *
	plotGenWBoson *
	genLeptons*
	plotGenLeptons*
        WCand*
        transverseW*
# 	printGenParticles*
# 	printGenLeptons*
        plotTransverseW

						 )


