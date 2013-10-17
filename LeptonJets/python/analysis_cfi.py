import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.ak5GenJets_cfi import *

otherLepton = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" ( abs(pdgId)==12 || abs(pdgId)==12 ) && status==1 & pt>5.0 ")
)

countFilter = cms.EDFilter("CandCountFilter",
								   src = cms.InputTag("otherLepton"),
								   minNumber = cms.uint32(1)
								   )


plotOtherLepton= cms.EDAnalyzer("CandViewHistoAnalyzer",
				src = cms.InputTag("otherLepton"),							   
 histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(300.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("olep_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("olep_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)




electron = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" abs(pdgId)==11 && status==1 ")
)

hv2 = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" abs(pdgId)==3000004 && status==1")
)



plothv2= cms.EDAnalyzer("CandViewHistoAnalyzer",
				src = cms.InputTag("hv2"),							   
 histograms = cms.VPSet(
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(10),
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(200.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("hv2_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    )
		)
)



plotMHT= cms.EDAnalyzer("CandViewHistoAnalyzer",
							src = cms.InputTag("MHT"),
 histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.),
	    max = cms.untracked.double(400.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("MHT"),
	    description = cms.untracked.string("MHT"),
	    plotquantity = cms.untracked.string("pt")
		)
)
)






MHT = cms.EDProducer("MHTProducer",
                                                        JetCollection = cms.InputTag("ak5GenJets"),
                                                        MinJetPt = cms.double(0.0),
                                                        MaxJetEta = cms.double(4.0)
                                                        )

electronGenJets = ak5GenJets.clone()
electronGenJets.src = cms.InputTag("electron")

 
plotMHT= cms.EDAnalyzer("CandViewHistoAnalyzer",
							src = cms.InputTag("MHT"),
 histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.),
	    max = cms.untracked.double(400.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("MHT"),
	    description = cms.untracked.string("MHT"),
	    plotquantity = cms.untracked.string("pt")
		)
)
)


plotGenJets= cms.EDAnalyzer("CandViewHistoAnalyzer",
				src = cms.InputTag("ak5GenJets"),							   
 histograms = cms.VPSet(
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(300.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("jet_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
		cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
		min = cms.untracked.double(0.0),
	    max = cms.untracked.double(50.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("jet_mass"),
	    description = cms.untracked.string("mass [GeV/c^2]"),
	    plotquantity = cms.untracked.string("mass")
	    ),
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("jet_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)

plotEJets= cms.EDAnalyzer("CandViewHistoAnalyzer",
				src = cms.InputTag("electronGenJets"),							   
 histograms = cms.VPSet(
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(100.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("ejet_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
		cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
		min = cms.untracked.double(0.0),
	    max = cms.untracked.double(12.0),
	    nbins = cms.untracked.int32(48),
	    name = cms.untracked.string("ejet_mass"),
	    description = cms.untracked.string("mass [GeV/c^2]"),
	    plotquantity = cms.untracked.string("mass")
	    ),
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("ejet_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)

analysis = cms.Sequence(
	otherLepton
	*countFilter
	*electron
						 *MHT
						 *electronGenJets
						 *plotMHT
						 *plotGenJets
						 *plotEJets
						 *hv2
						 *plothv2
	*plotOtherLepton
						 )

