import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    generator = cms.PSet(
        initialSeed = cms.untracked.uint32(123456789),
        engineName = cms.untracked.string('HepJamesRandom')
    )
)



process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('test.root')
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(18000) )

#process.source = cms.Source("EmptySource")

#process.load("CMSDAS2016.GenExercise.WjetsPy6_cff")

from Configuration.Generator.PythiaUESettings_cfi import *
process.source = cms.Source("LHESource",
        fileNames = cms.untracked.vstring(
	'file:test/7TeV_wjets_smzerobmass_run1001_unweighted_events_qcut20_mgPost.lhe')
)

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
	process.generator*~process.lfilter*
	process.genParticles*process.genParticlesForJets*process.ak5GenJets*
 	process.printGenParticles*
  	process.genParticlesClone *
	process.genWBoson *
	process.plotGenWBoson *

  process.rawmuons *

  process.rawelectrons *

  process.jets * process.otherLepton * process.plotOtherLepton

# process.selectedMuons *

# process.selectedElectrons *

# process.selectedJets *

# #process.met *

# process.countFilter *

# ~process.electronVeto *

# ~process.muonVeto *

# #process.jets0 *

# process.HT *

# process.MHT * 

# process.htSelect *
# process.mhtSelect *
# process.dphiSelect *


# 					 process.demo
					 )
