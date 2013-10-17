import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32(100)
)

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('SMSvalidation.root')
)


process.source = cms.Source("EmptySource")

from Configuration.Generator.PythiaUESettings_cfi import *

process.generator = cms.EDFilter("Pythia6GeneratorFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(12),
    comEnergy = cms.double(7000.0),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring(
"MSEL=0",
"IMSS(1)=11",
"MSTP(47)=0",   
"MSUB(243)=1",
"MSUB(244)=1",
		'IMSS(21) = 33            ! LUN number for SLHA File (must be 33) ',
		'IMSS(22) = 33            ! Read-in SLHA decay table '),
        SLHAParameters = cms.vstring(
		'SLHAFILE = UserCode/SMSScan/data/Exotica.slha'),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters','SLHAParameters')
    )
)


process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")

process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(5)
)

process.MessageLogger = cms.Service("MessageLogger",
    cout2 = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        )
    ),
    destinations = cms.untracked.vstring('cout2')
)

process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(
        generator = cms.untracked.uint32(1234567),
        g4SimHits = cms.untracked.uint32(123456788),
        VtxSmeared = cms.untracked.uint32(123456789)
    ),
)


process.genGluino = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" abs(pdgId)==1000021 && (status==3 || status==62) ")
)

process.plotGenGluino= cms.EDAnalyzer(
	"CandViewHistoAnalyzer",
	src = cms.InputTag("genGluino"),							   
	histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(300.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("gl_pT"),
	    description = cms.untracked.string("gl_pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("gl_rapidity"),
	    description = cms.untracked.string("gl_rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(800.0),
	    max = cms.untracked.double(1200.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("gl_mass"),
	    description = cms.untracked.string("gl_mass"),
	    plotquantity = cms.untracked.string("mass")
	    ),		
		)
)

process.genLeptons = cms.EDFilter("CandViewShallowCloneProducer",
  src = cms.InputTag("genParticles"),
  cut = cms.string(" ( abs(pdgId)==11 || abs(pdgId)==13 ) && status==1 && ( abs(mother(0).pdgId)==24  || abs(mother(0).pdgId)==23 || abs(mother(0).pdgId)==11 || abs(mother(0).pdgId)==13 ) ")
)


process.plotGenLeptons= cms.EDAnalyzer("CandViewHistoAnalyzer",
				src = cms.InputTag("genLeptons"),							   
 histograms = cms.VPSet(
	    cms.PSet(
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(300.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("lep_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
	    cms.PSet(
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("lep_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)


process.p = cms.Path(process.generator*process.genParticles
					 *process.printGenParticles*process.genGluino
					 *process.plotGenGluino
					 *process.genLeptons
					 *process.plotGenLeptons
					 )


process.schedule = cms.Schedule(process.p)


