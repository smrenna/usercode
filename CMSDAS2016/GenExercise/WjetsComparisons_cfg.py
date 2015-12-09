#import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Test")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'testpy6.root'
options.inputFiles = 'file:pythia8ex7.root'
options.maxEvents = -1 # -1 means all events

# get and parse the command line arguments
options.parseArguments()


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )




process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    generator = cms.PSet(
        initialSeed = cms.untracked.uint32(123456789),
        engineName = cms.untracked.string('HepJamesRandom')
    )
)


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputFile)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("PoolSource")
process.source.fileNames = cms.untracked.vstring(options.inputFiles)

#process.load("CMSDAS2012.GenExercise.WjetsPy6_cff")

# from Configuration.Generator.PythiaUESettings_cfi import *

# #from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *
# process.generator = cms.EDFilter("Pythia6GeneratorFilter",
#     maxEventsToPrint = cms.untracked.int32(5),
#     pythiaPylistVerbosity = cms.untracked.int32(1),
#     filterEfficiency = cms.untracked.double(1.0),
#     pythiaHepMCVerbosity = cms.untracked.bool(False),
#     comEnergy = cms.double(7000.0),
#     PythiaParameters = cms.PSet(
#         pythiaUESettingsBlock,
#         WjetsParameters = cms.vstring('MSEL=0',
#                         'MSUB(1)=1',
#                         '24:ALLOFF',
#                         '24:ONIFMATCH 11 13'),
#         parameterSets = cms.vstring('pythiaUESettings',
#             'WjetsParameters')
#     )
# )


process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")
process.load("CMSDAS2016.GenExercise.WjetsAnalysis_cfi")



process.p = cms.Path(
#	process.generator*
	process.genParticles*
	process.genParticlesForJets*
	
    process.analysis
	
					 )
