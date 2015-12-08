import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing


# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')


options.register ( "product",
                   "genParticles",
                    VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                    VarParsing.VarParsing.varType.string,          # string, int, or float
                    "Product names")

# setup any defaults you want
options.outputFile = 'testpy6.root'
options.inputFiles = 'file:pythia8ex7.root'
options.maxEvents = -1 # -1 means all events


#options.register ('product',
#  "genParticles",
#  VarParsing.multiplicity.singleton,
#  VarParsing.varType.string,
#  "Product to process")

# get and parse the command line arguments
options.parseArguments()

process = cms.Process("Test")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


#process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
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

for l in options.inputFiles:
   if l.find("MINIAOD")>-1:
      options.product="prunedGenParticles"
      break


print options.product

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



#process.load("RecoJets.Configuration.GenJetParticles_cff")
#process.load("RecoJets.JetProducers.ak5GenJets_cfi")
process.load("CMSDAS2016.GenExercise.ZjetsAnalysis_cfi")
process.genWBoson.src = cms.InputTag(options.product)
process.genLeptons.src = cms.InputTag(options.product)



process.p = cms.Path(
#	process.generator*
#	process.genParticles*
#	process.genParticlesForJets*
	
    process.analysis
	
					 )
