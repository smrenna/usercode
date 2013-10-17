import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('pythia88_3step.root')
)



process.source = cms.Source("EmptySource")

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(7000.),
    #useUserHook = cms.bool(True),
    PythiaParameters = cms.PSet(
        pythia8_example02 = cms.vstring('HiggsSM:ffbar2HW=on',
                                        '25:m0 = 120.0',
					'24:onMode = off',
					'24:onIfMatch = 11 12 ',
					'24:onIfMatch = 13 14 ',
					'24:onIfMatch = 15 16 ',
					'3000008:all = WHD4 void 1 0 0 10.0 .00001 0.0',
					'3000008:addChannel = 1 1.0 101  3000007 3000007',
					'3000007:all = WHD3 void 1 0 0 4.0 .00001 0.0',
					'3000007:addChannel = 1 1.0 101  3000006 3000006',
					'3000006:all = WHD2 void 1 0 0 1.0 .00001 0.0',
					'3000006:addChannel = 1 1.0 101  3000005 3000005',
					'3000005:all = WHD1 void 1 0 0 0.3 .00001 0.0',
				#	'3000005:addChannel = 1 0.065479 100  3000004 3000004',
				#	'3000005:addChannel = 1 0.934521 100  3000001 3000001',										
				 	'3000005:addChannel = 1 0.198500 100  3000004 3000004',
				 	'3000005:addChannel = 1 0.801500 100  3000001 3000001',										
					'3000004:all = WHD0  void 1 0 0 0.1 0.0 0.0',
					'3000001:all = ZDWID void 1 0 0 0.1 0.000001 0.0',										
					'3000001:addChannel = 1 0.1 101  11 -11',
					'25:onMode = off',
#'25:addChannel = 1  1.12622690e-02   101   3000005   3000005',
#'25:addChannel = 1  1.12608455e-02   101   3000006   3000006',
#'25:addChannel = 1  1.12373544e-02   101   3000007   3000007',
#'25:addChannel = 1  1.11048858e-02   101   3000008   3000008',
'25:addChannel = 1  1.00   101   3000008   3000008',
'PartonLevel:MI = off',
#'PartonLevel:FSRinResonances = off',
#					'111:mayDecay = false'
#										'SLHA:readFrom = 2',
#										'SLHA:file = darktest.slha'
										),
        parameterSets = cms.vstring('pythia8_example02')
    )
)

process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        )
    ),
    destinations = cms.untracked.vstring('cout')
)

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(
        generator = cms.untracked.uint32(123456),
        g4SimHits = cms.untracked.uint32(123456788),
        VtxSmeared = cms.untracked.uint32(123456789)
    ),
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20000)
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


process.p = cms.Path(process.generator
					 *process.genParticles
					 *process.genParticlesForJets
					 *process.ak5GenJets
					 *process.analysis
					 *process.printGenParticles
					 *process.printElectrons
#					 *process.demo
					 )
process.outpath = cms.EndPath(process.GEN)

#process.schedule = cms.Schedule(process.p, process.outpath)
process.schedule = cms.Schedule(process.p)


