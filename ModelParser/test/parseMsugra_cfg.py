import FWCore.ParameterSet.Config as cms

from Configuration.Generator.PythiaUESettings_cfi import *

process = cms.Process("TEST")
process.load("FWCore.Framework.test.cmsExceptionsFatal_cff")
process.load("Configuration.StandardSequences.Services_cff")



# The following three lines reduce the clutter of repeated printouts
# of the same exception message.
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.destinations = ['cerr']
process.MessageLogger.statistics = []
process.MessageLogger.fwkJobReports = []
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(30001))

process.source = cms.Source("PoolSource",
  fileNames=cms.untracked.vstring('/store/mc/Summer11/mSUGRA_m0-20to2000_m12-20to760_tanb-10andA0-0_7TeV-Pythia6Z/AODSIM/PU_S4_START42_V11_FastSim-v1/0000/001BCCDC-56A3-E011-BC14-0030486790A0.root')
)


process.PARSE = cms.EDFilter("ModelParser")

process.p = cms.Path(process.PARSE)

process.schedule = cms.Schedule(process.p)
