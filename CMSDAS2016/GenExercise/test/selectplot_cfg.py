import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("Demo")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'selectplot.root'
options.inputFiles = 'file:pythia8ex7.root'
options.maxEvents = -1 # -1 means all events

# get and parse the command line arguments
options.parseArguments()

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.source = cms.Source("PoolSource")
process.source.fileNames = cms.untracked.vstring(options.inputFiles)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputFile)
)

product="genParticles"
for l in options.inputFiles:
   if l.find("MINIAOD")>-1:
      product="prunedGenParticles"
      break

process.genParticlesClone = cms.EDFilter("CandViewShallowCloneProducer",
    src = cms.InputTag(product),
    cut = cms.string("status=2 & ((abs(pdgId)>500 & abs(pdgId)<600) || (abs(pdgId)>5000 & abs(pdgId)<6000) ) ")
)


process.plotBHadrons= cms.EDAnalyzer("CandViewHistoAnalyzer",
    src = cms.InputTag("genParticlesClone"),
    histograms = cms.VPSet(
        cms.PSet(
            min = cms.untracked.double(0.0),
            max = cms.untracked.double(200.0),
            nbins = cms.untracked.int32(50),
            name = cms.untracked.string("bHadron pT"),
            description = cms.untracked.string("p_{T} [GeV/c]"),
            plotquantity = cms.untracked.string("pt")
        )
    )
)


process.p = cms.Path(process.genParticlesClone*process.plotBHadrons)

