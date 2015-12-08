import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Demo")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'testpy6.root'
options.inputFiles = 'file:pythia8ex7.root'
options.maxEvents = 1 # -1 means all events

# get and parse the command line arguments
options.parseArguments()


process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.source = cms.Source("PoolSource")
process.source.fileNames = cms.untracked.vstring(options.inputFiles)

product="genParticles"
for l in options.inputFiles:
   if l.find("MINIAOD")>-1:
      product="prunedGenParticles"
      break


process.printGenParticle = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag(str(product)),
     maxEventsToPrint = cms.untracked.int32(-1)
)

process.p = cms.Path(process.printGenParticle)
