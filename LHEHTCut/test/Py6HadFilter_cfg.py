import FWCore.ParameterSet.Config as cms

from Configuration.Generator.PythiaUESettings_cfi import *

process = cms.Process("TEST")
process.load("FWCore.Framework.test.cmsExceptionsFatal_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")

process.load("Configuration.StandardSequences.Services_cff")

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    generator = cms.PSet(
        initialSeed = cms.untracked.uint32(123456789),
        engineName = cms.untracked.string('HepJamesRandom')
    )
)

process.randomEngineStateProducer = cms.EDProducer("RandomEngineStateProducer")

# The following three lines reduce the clutter of repeated printouts
# of the same exception message.
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.destinations = ['cerr']
process.MessageLogger.statistics = []
process.MessageLogger.fwkJobReports = []

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(50))

process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring('file:ttbar_5flavours_xqcut20_10TeV.lhe')
)

process.generator = cms.EDFilter("Pythia6HadronizerFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(5),
    pythiaPylistVerbosity = cms.untracked.int32(7),
    comEnergy = cms.double(10000.0),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring('MSEL=0         ! User defined processes', 
                        'PMAS(5,1)=4.4   ! b quark mass',
                        'PMAS(6,1)=172.4 ! t quark mass',
			'MSTJ(1)=0       ! Fragmentation/hadronization on or off',
                        'MSTP(71)=0','MSTP(81)=0','MSTP(91)=0',
			'MSTP(61)=0      ! Parton showering on or off'),
        # This is a vector of ParameterSet names to be read, in this order
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters')
    )
)

process.printEvents = cms.EDAnalyzer("ParticleListDrawer",
   src=cms.InputTag("genParticles"),
   maxEventsToPrint = cms.untracked.int32(5)
)

process.htcut = cms.EDFilter("LHEHTCut",
   LHEHTCut = cms.double(200.0)
)


process.p = cms.Path(process.generator*process.genParticles*process.htcut*process.printEvents)
process.p1 = cms.Path(process.randomEngineStateProducer)

process.schedule = cms.Schedule(process.p, process.p1)
