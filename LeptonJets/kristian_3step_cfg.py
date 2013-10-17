import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('bridge_3step.root')
)


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_7078_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_7118_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_7345_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_7842_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_8545_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_8877_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_9031_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_9055_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_929_darkstuff.root',
'dcap://pnfs/cms/WAX/resilient/kristian/darkstuff/RECO/reco_962_darkstuff.root'	)
)															 
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')


process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        default = cms.untracked.PSet(
  #          limit = cms.untracked.int32(0)
        )
    ),
    destinations = cms.untracked.vstring('cout')
)



process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(10)
)

process.printElectrons = cms.EDAnalyzer("ParticleListDrawer",
#     src = cms.InputTag("genParticles"),
     src = cms.InputTag("electron"),
     maxEventsToPrint = cms.untracked.int32(10)
)

process.GEN = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('pythia8ex2.root')
)

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")
process.load('UserCode.LeptonJets.leptonjets_cfi')
process.load('UserCode.LeptonJets.analysis_cfi')

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.genParticlesForJets.ignoreParticleIDs.extend(cms.vuint32(3000004,11,12,13,14,15,16))
process.load("RecoJets.JetProducers.ak5GenJets_cfi")

process.demo = cms.EDAnalyzer("LeptonJets")

process.p = cms.Path(
#	process.generator
#					 *process.genParticles
					 process.genParticlesForJets
					 *process.ak5GenJets
					 *process.analysis
					 *process.printGenParticles
					 *process.printElectrons
#					 *process.demo
					 )
process.outpath = cms.EndPath(process.GEN)

#process.schedule = cms.Schedule(process.p, process.outpath)
process.schedule = cms.Schedule(process.p)


