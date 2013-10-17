output = False
fromreco = False
genseed = True 
fullsim = False
fastsim = True


import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32(-1)
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('validation.root')
)


process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring('/store/mc/Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v2/0000/00FA42AB-D1A9-E011-B6A2-003048678FD6.root')
)


process.generator = cms.EDProducer(
  "TauGun",
  SeedSrc = cms.InputTag("genWCand"),
  VtxSrc = cms.InputTag("offlinePrimaryVertices"),
  GenSrc = cms.InputTag("genWCand"),
  GenSeed = cms.bool(True),
  UseTauola = cms.bool(True),
  FixedSeed = cms.bool(False),
  FixedCharge = cms.int32(-1),
  FixedEta = cms.double(0),
  FixedPhi = cms.double(0),
  FixedEnergy = cms.double(50),
  FixedVtxX = cms.double(0.05),
  FixedVtxY = cms.double(-10),
  FixedVtxZ = cms.double(5),
  pythiaHepMCVerbosity = cms.untracked.bool(True),
  pythiaPylistVerbosity = cms.untracked.int32(1),
  maxEventsToPrint = cms.untracked.int32(100),
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
    mdtau = cms.int32(240) # all taus only hadronic ; changed from 230
  )
)

process.tauDecays1 = cms.EDFilter("CandViewSelector",
  src = cms.InputTag("genParticles::HLT"),
  cut = cms.string(" status==1 && abs(mother(0).pdgId)==15 ")
)

process.countFilter1 = cms.EDFilter("CandCountFilter",
								   src = cms.InputTag("tauDecays1"),
								   minNumber = cms.uint32(2),maxNumber=cms.uint32(2)
								   )

process.tauDecays1a = cms.EDFilter("CandViewSelector",
  src = cms.InputTag("tauDecays1"),
  cut = cms.string(" status==1 && abs(pdgId)==211 ")
)

process.countFilter1a = cms.EDFilter("CandCountFilter",
								   src = cms.InputTag("tauDecays1a"),
								   minNumber = cms.uint32(1),maxNumber=cms.uint32(1)
								   )

process.tauDecays2 = cms.EDFilter("CandViewSelector",
  src = cms.InputTag("genParticles::PROD"),
  cut = cms.string(" status==1 && abs(mother(0).pdgId)==15 && abs(pdgId)==211")
)

process.plotDecay1= cms.EDAnalyzer(
	"CandViewHistoAnalyzer",
	src = cms.InputTag("tauDecays1a"),							   
	histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(1.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("x"),
	    description = cms.untracked.string("x"),
	    plotquantity = cms.untracked.string("energy/mother(0).energy")
	    )
	   )
   )


process.plotDecay2= cms.EDAnalyzer(
	"CandViewHistoAnalyzer",
	src = cms.InputTag("tauDecays2"),							   
	histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(1.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("x"),
	    description = cms.untracked.string("x"),
	    plotquantity = cms.untracked.string("energy/mother(0).energy")
	    )
	   )
   )



process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("tauDecays1a"),
     maxEventsToPrint = cms.untracked.int32(10)
)

process.printGenParticles2 = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("tauDecays2"),
     maxEventsToPrint = cms.untracked.int32(10)
)

process.genTauLeptons = cms.EDFilter("CandViewSelector",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" abs(pdgId)==15 && status==2 && ( abs(mother(0).pdgId)==24  || abs(mother(0).pdgId)==15 ) ")
)

process.genTauNeutrinos = cms.EDFilter("CandViewSelector",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" abs(pdgId)==16 && status==1 && ( abs(mother(0).pdgId)==24  || abs(mother(0).pdgId)==16 ) ")
)

# merge leptons and neutrino into W candidates
process.genWCand = cms.EDProducer("CandMerger",
   src = cms.VInputTag("genTauLeptons", "genTauNeutrinos")
)


process.tauFilter = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" abs(pdgId)==15 && (status==3 || status==62) ")								 
)
 
process.countFilter = cms.EDFilter("CandCountFilter",
								   src = cms.InputTag("tauFilter"),
								   minNumber = cms.uint32(1),maxNumber=cms.uint32(1)
								   )


### --- Paths -------------------------

if genseed:
  process.p = cms.Path(process.tauFilter*process.countFilter*
      process.genTauNeutrinos
    + process.genTauLeptons     
    + process.genWCand
    + process.generator
    + process.genParticles
    + process.tauDecays2
    + process.printGenParticles2                       
    + process.plotDecay2
    + process.tauDecays1
    + process.countFilter1
    + process.tauDecays1a
    + process.printGenParticles                       
    + process.countFilter1a                       
    + process.plotDecay1                     
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
#  if fastsim:
#    process.p = cms.Path(
#        process.tauGunSplit
#      + process.countPFMu
#      + process.generator
#      + process.famosWithEverything
#      + process.tauGunMerge
#     )

if output:
  process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('tauguntest.root'),
    outputCommands = cms.untracked.vstring('keep *'),
#    SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
#    dropMetaData = cms.untracked.string("DROPPED")
  )
  process.outpath = cms.EndPath(
    process.out
  )


#dumpFile  = open("tauguntestfull.py", "w")
#dumpFile.write(process.dumpPython())
#dumpFile.close()
