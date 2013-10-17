
import FWCore.ParameterSet.Config as cms

generator = cms.EDProducer(
  "TauGun",
  SeedSrc = cms.InputTag("tauGunSplit:pfMu"),
  VtxSrc = cms.InputTag("offlinePrimaryVertices"),
  GenSrc = cms.InputTag("genParticles::HLT"),
  GenSeed = cms.bool(False),
  FixedSeed = cms.bool(False),
  FixedCharge = cms.int32(-1),
  FixedEta = cms.double(0),
  FixedPhi = cms.double(0),
  FixedEnergy = cms.double(50),
  FixedVtxX = cms.double(0.05),
  FixedVtxY = cms.double(-10),
  FixedVtxZ = cms.double(5),
  pythiaHepMCVerbosity = cms.untracked.bool(False),
  pythiaPylistVerbosity = cms.untracked.int32(0),
  maxEventsToPrint = cms.untracked.int32(0),
  PythiaParameters = cms.PSet(
    pythiaTauJets = cms.vstring(
#      'MDCY(15,1)=0 ! sets tau stable so that taula will decay it'
    ),
    parameterSets = cms.vstring(
      'pythiaTauJets'
    )
  ),
  UseTauolaPolarization = cms.bool(True),
  InputCards = cms.PSet(
    pjak1 = cms.int32(0),
    pjak2 = cms.int32(0),
    mdtau = cms.int32(230) # all taus only hadronic
  )
) 

# the full sequence for fullsim would look like this:
#
# process.load('Configuration.StandardSequences.Services_cff')
# process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
# process.load('FWCore.MessageService.MessageLogger_cfi')
# process.load('Configuration.EventContent.EventContent_cff')
# process.load('SimGeneral.MixingModule.mixNoPU_cfi')
# process.load('Configuration.StandardSequences.GeometryDB_cff')
# process.load('Configuration.StandardSequences.MagneticField_38T_cff')
# process.load('Configuration.StandardSequences.Generator_cff')
# process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic7TeV2011Collision_cfi')
# process.load('GeneratorInterface.Core.genFilterSummary_cff')
# process.load('Configuration.StandardSequences.SimIdeal_cff')
# process.g4SimHits.NonBeamEvent = True
# process.load('Configuration.StandardSequences.Digi_cff')
# process.load('Configuration.StandardSequences.SimL1Emulator_cff')
# process.load('Configuration.StandardSequences.DigiToRaw_cff')
# process.load('Configuration.StandardSequences.RawToDigi_cff')
# process.load('Configuration.StandardSequences.Reconstruction_cff')
# process.load('Configuration.StandardSequences.EndOfProcess_cff')
# process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# process.GlobalTag.globaltag   = 'START42_V15B::All'
#
# process.p = cms.Path(
#     ...
#   + process.generator
#   + process.pgen
#   + process.psim
#   + process.pdigi
#   + process.SimL1Emulator
#   + process.DigiToRaw
#   + process.RawToDigi
#   + process.reconstruction
#   + ...
# )

# the full sequence for fastsim would look like this:
#
# process.load("FastSimulation/Configuration/RandomServiceInitialization_cff")
# process.load('FastSimulation.Configuration.Geometries_cff')
# process.load("Configuration.StandardSequences.MagneticField_38T_cff")
# process.VolumeBasedMagneticFieldESProducer.useParametrizedTrackerField = True
# process.load("FastSimulation/Configuration/FamosSequences_cff")
# process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# process.GlobalTag.globaltag   = 'START42_V15B::All'
#
# process.p = cms.Path(
#     ...
#   + process.generator
#   + process.famosWithEverything
#   + ...
# )
