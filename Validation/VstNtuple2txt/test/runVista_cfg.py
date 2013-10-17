import FWCore.ParameterSet.Config as cms

process = cms.Process("VISTA")
process.load("FWCore.Framework.test.cmsExceptionsFatal_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
#process.load("PhysicsTools.HepMCCandAlgos.genParticlesForJets_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")


from RecoJets.JetProducers.ak5GenJets_cfi import *


process.load("RecoJets.Configuration.GenJetParticles_cff")




# The following three lines reduce the clutter of repeated printouts
# of the same exception message.
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.destinations = ['cerr']
process.MessageLogger.statistics = []
process.MessageLogger.fwkJobReports = []

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
  'file://TestOSET.root'
        )
)



process.demo = cms.EDAnalyzer("Ntuple2txt",
   fileName_ = cms.string('test.txt')
)


process.genVista = cms.EDProducer("VstParticleCandidateSelector",
    src = cms.InputTag("genParticles"),
    verbose = cms.untracked.bool(False),
    stableOnly = cms.bool(False),
    etaMaxShower = cms.untracked.double(4.0),
    etaMaxParticle = cms.untracked.double(4.0)
)



process.VistaJet = ak5GenJets.clone()
process.VistaJet.src = cms.InputTag("genVista:partonShowerVst")


process.VistaTauJet = ak5GenJets.clone()
process.VistaTauJet.src = cms.InputTag("genVista:tauVst")
process.VistaTauJet.rParam = cms.double(0.1)


process.VistaJetClone = cms.EDProducer("GenJetShallowCloneProducer",
    src = cms.InputTag("VistaJet")
 )

process.particleJetMatch = cms.EDProducer("TrivialDeltaRMatcher",
    matched = cms.InputTag("VistaJetClone"),
    src = cms.InputTag("genVista:otherStableVst"),
    distMin = cms.double(0.8)
)


process.printGenParticle = cms.EDAnalyzer("ParticleListDrawer",
    src = cms.InputTag("genParticles"),
    maxEventsToPrint = cms.untracked.int32(5)
)


process.printVistaJet = cms.EDAnalyzer("ParticleListDrawer",
    src = cms.InputTag("VistaJetClone"),
    maxEventsToPrint = cms.untracked.int32(5)
)

process.printOtherStableVst = cms.EDAnalyzer("ParticleListDrawer",
    src = cms.InputTag("genVista:otherStableVst"),
    maxEventsToPrint = cms.untracked.int32(5)
)

process.mergerVst = cms.EDProducer("CandMerger",
   src = cms.VInputTag("genVista:electronVst", "genVista:muonVst", "genVista:photonVst")
)


process.p = cms.Path(
	process.genParticles
	*process.genParticlesForJets
	*process.genVista
					 *process.ak5GenJets
					 *process.VistaJet
					 *process.VistaJetClone
					 *process.particleJetMatch
					 *process.mergerVst
					 *process.demo
					 )

process.schedule = cms.Schedule(process.p)
