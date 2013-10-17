
output = True
fromreco = False
genseed = False
fullsim = False
fastsim = True

if not (fastsim is not fullsim):
  print "Either select fullsim or fastsim. Exiting."
  exit

import FWCore.ParameterSet.Config as cms

process = cms.Process("CLEAN")

# logging options
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport  = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(100),
    limit = cms.untracked.int32(1)
)
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

#process.Tracer = cms.Service("Tracer") 

# Input
import glob
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.source = cms.Source(
  "PoolSource",
  fileNames = cms.untracked.vstring(
    "file:hotskim.root"
  ),
  inputCommands = cms.untracked.vstring( "keep *", "drop *_MEtoEDMConverter_*_*", "drop *_lumiProducer_*_*" )
)
if fromreco:
  process.source.fileNames = cms.untracked.vstring("file:/data/lowette/mergejitest.root")
if genseed:
  process.source.fileNames = cms.untracked.vstring(
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_100_1_QY9.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_101_1_hCK.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_102_1_HC7.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_103_1_2Am.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_104_1_Xd1.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_105_1_XkD.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_107_1_IyV.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_108_1_wP4.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_109_1_pFB.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_10_1_3EF.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_110_1_Gsh.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_111_1_xXD.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_112_1_w3j.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_113_1_iSz.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_114_3_Ii7.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_115_1_1UD.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_116_1_AsV.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_117_1_g71.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_118_1_YqD.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_119_1_AKW.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_11_1_6py.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_121_1_Kiw.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_122_1_8Ir.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_123_1_cru.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_124_1_Gpw.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_125_1_9SK.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_126_4_iF5.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_128_1_cIa.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_12_1_C9C.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_131_1_CGy.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_132_1_EPf.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_133_1_JEd.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_134_1_jDO.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_135_1_VYG.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_136_1_SAi.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_137_1_gBN.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_138_1_6k0.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_139_1_JrX.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_13_1_mf5.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_140_1_akr.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_141_1_ZDz.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_142_1_35J.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_143_1_qng.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_144_1_8mX.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_145_1_kdE.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_146_1_y0f.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_147_3_du9.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_148_1_frR.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_149_2_shJ.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_14_1_Jy4.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_150_3_Gl1.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_151_1_gJa.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_15_1_J77.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_16_1_Wa5.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_17_1_K1Z.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_18_1_Fm5.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_19_1_mVV.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_1_1_hpo.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_21_1_OwH.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_22_1_Hzq.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_24_1_VrO.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_25_1_arA.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_26_1_LXk.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_27_1_mXT.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_28_1_R3g.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_29_1_Bbz.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_2_1_gXn.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_30_1_KKI.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_31_1_eUS.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_32_1_Z9V.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_33_1_2gb.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_34_1_QpS.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_35_1_0cu.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_36_1_kxQ.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_37_1_jP1.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_38_1_YYJ.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_3_1_2Ji.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_40_1_k54.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_41_1_Q0A.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_44_2_8T8.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_45_1_PPX.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_46_1_MkM.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_49_1_CcB.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_4_1_nJy.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_50_1_Ox2.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_51_1_HNf.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_52_1_DRi.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_53_1_ZgS.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_54_1_BHi.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_55_1_LVR.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_56_1_Son.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_57_1_lAL.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_58_1_fcD.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_59_3_8oP.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_5_1_uFb.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_60_1_6QK.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_61_1_pXI.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_62_1_O2N.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_65_1_vPH.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_66_1_95p.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_67_1_jHs.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_68_3_z43.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_69_1_LLD.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_6_1_WiA.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_70_1_GJW.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_71_1_Xub.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_72_1_H0V.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_73_1_Fw7.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_75_4_W1t.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_76_1_Mgp.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_77_1_LBv.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_78_1_fwy.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_79_2_Lah.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_7_1_V4Q.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_81_3_reo.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_82_3_qFx.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_83_6_jKe.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_84_1_bu4.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_85_1_FfF.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_86_1_Qgl.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_87_1_UIW.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_88_1_o4F.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_89_1_9ou.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_8_1_BCF.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_90_1_9bS.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_91_2_7wu.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_92_1_760.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_93_1_kzk.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_94_3_I1q.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_95_6_ohd.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_96_1_PhF.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_97_1_zS7.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_98_1_74S.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_99_1_UCl.root',
    'file:/data/dalfonso/copyMC_428_met/copyMET150_PAT_TTbar_9_1_Vt3.root',
  )


process.tauGunSplit = cms.EDProducer(
  "TauGunSplitter",
  PFSource = cms.InputTag("pfNoPileUpPFchs"),
  TrackSource = cms.InputTag("generalTracks"),
  VertexSource = cms.InputTag("offlinePrimaryVertices"),
)
process.countPFMu = cms.EDFilter(
  "CandViewCountFilter",
  src = cms.InputTag("tauGunSplit:pfMu"),
  minNumber = cms.uint32(1),
  maxNumber = cms.uint32(1)
)


process.generator = cms.EDProducer(
  "TauGun",
  SeedSrc = cms.InputTag("tauGunSplit:pfMu"),
  VtxSrc = cms.InputTag("offlinePrimaryVertices"),
  GenSrc = cms.InputTag("genParticles::HLT"),
  GenSeed = cms.bool(genseed),
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

if fullsim:
  process.load('Configuration.StandardSequences.Services_cff')
  process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
  process.load('FWCore.MessageService.MessageLogger_cfi')
  process.load('Configuration.EventContent.EventContent_cff')
  process.load('SimGeneral.MixingModule.mixNoPU_cfi')
  process.load('Configuration.StandardSequences.GeometryDB_cff')
  process.load('Configuration.StandardSequences.MagneticField_38T_cff')
  process.load('Configuration.StandardSequences.Generator_cff')
  process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic7TeV2011Collision_cfi')
  process.load('GeneratorInterface.Core.genFilterSummary_cff')
  process.load('Configuration.StandardSequences.SimIdeal_cff')
  process.g4SimHits.NonBeamEvent = True
  process.load('Configuration.StandardSequences.Digi_cff')
  process.load('Configuration.StandardSequences.SimL1Emulator_cff')
  process.load('Configuration.StandardSequences.DigiToRaw_cff')
  process.load('Configuration.StandardSequences.RawToDigi_cff')
  process.load('Configuration.StandardSequences.Reconstruction_cff')
  process.load('Configuration.StandardSequences.EndOfProcess_cff')
if fastsim:
  process.load("FastSimulation/Configuration/RandomServiceInitialization_cff")
  process.load('FastSimulation.Configuration.Geometries_cff')
  process.load("Configuration.StandardSequences.MagneticField_38T_cff")
  process.VolumeBasedMagneticFieldESProducer.useParametrizedTrackerField = True
  process.load("FastSimulation/Configuration/FamosSequences_cff")
if fullsim or fastsim:
  process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
  process.GlobalTag.globaltag   = 'START42_V15B::All'


process.tauGunMerge = cms.EDProducer(
  "TauGunMerger",
  pfsrc1 = cms.InputTag("tauGunSplit:pfNoMu"),
  pfsrc2 = cms.InputTag("particleFlow"), # will take the latest one, from the taus
  trsrc1 = cms.InputTag("tauGunSplit:tracksNoMu"),
  trsrc2 = cms.InputTag("generalTracks"), # will take the latest one, from the taus
  vtxsrc = cms.InputTag("offlinePrimaryVertices::RECO"), # important to take the ones from RECO!!!
)


process.hadtaufilter = cms.EDFilter(
  "TtbarDecayFilter",
  GenParticleSrc = cms.InputTag("genParticles::HLT"),
  BoolSrc = cms.vint32(0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
)
process.TFileService = cms.Service(
  "TFileService",
  fileName = cms.string("taugunvalidation.root")
)
process.plotter = cms.EDAnalyzer(
  "GenTauPlotter",
  GenSrc1 = cms.InputTag("genParticles::HLT"),
  GenSrc2 = cms.InputTag("genParticles::CLEAN")
)



### --- Paths -------------------------

if genseed:
  process.p = cms.Path(
      process.hadtaufilter
    + process.generator
    + process.pgen
    + process.plotter  # for testing
  )

if not genseed:
  if fullsim:
    process.p = cms.Path(
        process.tauGunSplit
      + process.countPFMu
      + process.generator
      + process.pgen
      + process.psim
      + process.pdigi
      + process.SimL1Emulator
      + process.DigiToRaw
      + process.RawToDigi
      + process.reconstruction
      + process.tauGunMerge
    )
  if fastsim:
    process.p = cms.Path(
        process.tauGunSplit
      + process.countPFMu
      + process.generator
      + process.famosWithEverything
      + process.tauGunMerge
    )

if output:
  process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tauguntest.root'),
    outputCommands = cms.untracked.vstring('keep *'),
    SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    dropMetaData = cms.untracked.string("DROPPED")
  )
  process.outpath = cms.EndPath(
    process.out
  )


#dumpFile  = open("tauguntestfull.py", "w")
#dumpFile.write(process.dumpPython())
#dumpFile.close()
