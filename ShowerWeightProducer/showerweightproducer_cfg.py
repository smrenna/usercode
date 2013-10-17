import FWCore.ParameterSet.Config as cms

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# The following three lines reduce the clutter of repeated printouts
# of the same exception message.
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.destinations = ['cerr']
process.MessageLogger.statistics = []
process.MessageLogger.fwkJobReports = []
process.MessageLogger.cerr.FwkReport.reportEvery = 10000



process.source = cms.Source("PoolSource",
#fileNames = cms.untracked.vstring('/store/mc/Summer12/DYJetsToLL_M-50_scaleup_8TeV-madgraph-tauola/AODSIM/START52_V9_FSIM-v1/00000/0228D060-51F2-E111-BB68-003048FFD720.root')
#fileNames = cms.untracked.vstring('/store/mc/Summer12/DYJetsToLL_M-50_scaleup_8TeV-madgraph-tauola/AODSIM/START52_V9_FSIM-v1/00000/0228D060-51F2-E111-BB68-003048FFD720.root')
#fileNames = cms.untracked.vstring('file:../ShowerWeight/pyex.root'),
							
####fileNames = cms.untracked.vstring('file:../TestIt/pythia1_save.root'),
fileNames = cms.untracked.vstring(
#"dcap:///cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/lpcsusyhad/53X_ntuples/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/vchetlur/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/67e73f866d34072a7aee49050064a888//susypat_286_1_sJz.root"),
"dcap:///cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/lpcsusyhad/53X_ntuples/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/vchetlur/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/67e73f866d34072a7aee49050064a888//susypat_371_1_1Vz.root",
"dcap:///cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/lpcsusyhad/53X_ntuples/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/vchetlur/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/67e73f866d34072a7aee49050064a888//susypat_22_1_nws.root",
       "dcap:///cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/lpcsusyhad/53X_ntuples/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/vchetlur/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/67e73f866d34072a7aee49050064a888//susypat_219_1_5KL.root",
       "dcap:///cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/lpcsusyhad/53X_ntuples/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/vchetlur/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/67e73f866d34072a7aee49050064a888//susypat_199_1_v2s.root",
       "dcap:///cmsdca.fnal.gov:24136/pnfs/fnal.gov/usr/cms/WAX/11/store/user/lpcsusyhad/53X_ntuples/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/vchetlur/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph-v2_lpc1/67e73f866d34072a7aee49050064a888//susypat_304_1_hhB.root"),
skipEvents = cms.untracked.uint32(0)
)


process.myWeightProducer = cms.EDProducer('ShowerWeightProducer',
parameterSource = cms.string("SIM")
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('newFile.root'),
    outputCommands = cms.untracked.vstring('drop *', 
         'keep *_*_weight_*',
    ),
)

process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(0)
)


  
process.p = cms.Path(process.printGenParticles*process.myWeightProducer)

#process.e = cms.EndPath(process.out)
