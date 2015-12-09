# import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("USER")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'wplusjets.root'
options.inputFiles = '/store/user/cmsdas/2012/GenShortExercise/WplusToENu_M-20_CT10_TuneZ2_7TeV-powheg-pythia-0.root'
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

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(7000.),
    emissionVeto = cms.untracked.PSet(),
    PythiaParameters = cms.PSet(
        pythia8_example07 = cms.vstring('SpaceShower:pTmaxMatch = 2',
                                        'TimeShower:pTmaxMatch  = 2'),
        parameterSets = cms.vstring('pythia8_example07')
    )
)


process.wfilter = cms.EDFilter("MCSingleParticleFilter",
         Status = cms.untracked.vint32(3),
     MaxEta = cms.untracked.vdouble(200.0),
     MinEta = cms.untracked.vdouble(-200.0),
     MinPt = cms.untracked.vdouble(0.0),
     ParticleID = cms.untracked.vint32(24)
)



process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")
process.load("CMSDAS2016.GenExercise.WjetsAnalysis_cfi")



process.p = cms.Path(
	process.generator*
#        process.wfilter*
	process.genParticles*
	process.genParticlesForJets*
	process.genParticlesForJetsNoNu*
        process.analysis
					 )
