import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
#        '/store/user/cmsdas/OSETExercise/t_b_H.root'
        'file:t_b_H_0.root'
    )
)

process.printGenParticle = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(1)
)



process.genParticlesClone = cms.EDFilter("CandViewShallowCloneProducer",
										 src = cms.InputTag("genParticles"),
										 cut = cms.string("!charge = 0 & status=1")
										 )

process.genTopClone = cms.EDFilter("CandViewShallowCloneProducer",
										 src = cms.InputTag("genParticles"),
										 cut = cms.string("pdgId = 6 & status=3")
										 )


process.printGenParticle = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticlesClone"),
     maxEventsToPrint = cms.untracked.int32(1)
)



process.chargedHistos= cms.EDAnalyzer("CandViewHistoAnalyzer",
							src = cms.InputTag("genParticlesClone"),
 histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(20.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("charged track pT"),
	    description = cms.untracked.string("pT [GeV/c"),
	    plotquantity = cms.untracked.string("pt")
	    )
		)
)

process.TFileService = cms.Service(
     "TFileService",
     fileName = cms.string("selectplot.root")
)


process.p = cms.Path(process.genParticles*process.genParticlesClone*process.printGenParticle*process.chargedHistos)

