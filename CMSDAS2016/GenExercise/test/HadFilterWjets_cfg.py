#import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("USER")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'wplusjets.root'
options.inputFiles = '/store/user/cmsdas/2012/GenShortExercise/7TeV_wjets_smzerobmass_run1001_unweighted_events_qcut20_mgPost.lhe'
options.maxEvents = -1 # -1 means all events

# get and parse the command line arguments
options.parseArguments()


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.suppressWarning = cms.untracked.vstring('source','Generator','LHEInterface')
process.MessageLogger.suppressInfo = cms.untracked.vstring('Generator','LHEInterface')
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

process.source = cms.Source("LHESource")
process.source.fileNames = cms.untracked.vstring(options.inputFiles)

#process.load("CMSDAS2016.GenExercise.WjetsPy6_cff")
from Configuration.Generator.PythiaUESettings_cfi import *

process.generator = cms.EDFilter("Pythia6HadronizerFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(True),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    comEnergy = cms.double(7000.0),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring('MSEL=0         ! User defined processes',
                        'PMAS(5,1)=4.8   ! b quark mass',
                        'PMAS(6,1)=172.5 ! t quark mass',
                        'MSTJ(1)=       ! Fragmentation/hadronization on or off',
                        'MSTP(61)=      ! Parton showering on or off'),
        # This is a vector of ParameterSet names to be read, in this order
        parameterSets = cms.vstring('pythiaUESettings',
            'processParameters')
    ),
    jetMatching = cms.untracked.PSet(
       scheme = cms.string("Madgraph"),
       mode = cms.string("auto"),       # soup, or "inclusive" / "exclusive"
       MEMAIN_nqmatch = cms.int32(4),
       MEMAIN_etaclmax = cms.double(-1),
       MEMAIN_qcut = cms.double(-1),
       MEMAIN_minjets = cms.int32(-1),
       MEMAIN_maxjets = cms.int32(-1),
       MEMAIN_showerkt = cms.double(0),
       MEMAIN_excres = cms.string(""),
       outTree_flag = cms.int32(0)        # 1=yes, write out the tree for future sanity check
    )
)

process.lfilter = cms.EDFilter("MCSingleParticleFilter",
         Status = cms.untracked.vint32(3,3),
     MaxEta = cms.untracked.vdouble(200.0, 200.0),
     MinEta = cms.untracked.vdouble(-200.0, -200.0),
     MinPt = cms.untracked.vdouble(0.0, 0.0),
     ParticleID = cms.untracked.vint32(15,-15)
)


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
	process.generator*
	process.genParticles*
        ~process.lfilter*
#	process.genParticlesForJets*
	process.genParticlesForJetsNoNu*
        process.analysis
					 )
