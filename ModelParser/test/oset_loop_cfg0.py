import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.TFileService = cms.Service(
     "TFileService",
     fileName = cms.string("TN_out.0.root")
)

process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32(10000)
)


process.source = cms.Source("EmptySource")

from Configuration.Generator.PythiaUEZ2Settings_cfi import *


process.generator = cms.EDFilter("Pythia6GeneratorFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    comEnergy = cms.double(7000.0),
    pythiaToLHE = cms.bool(True),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring(
'MSEL=0         ! User defined processes',
'MSTP(161)=67',
'MSTP(162)=68',
'MSTP(163)=69',
'IMSS(1) = 11             ! Spectrum from external SLHA file',
'MSUB(243)=1              ',
'MSUB(244)=1              ',
'IMSS(21) = 33            ! LUN number for SLHA File (must be 33) ',
'IMSS(22) = 33            ! Read-in SLHA decay table '),
        SLHAParameters = cms.vstring(
		'SLHAFILE =  UserCode/ModelParser/test/TN_475.0_353.42_275.0.slha'),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters','SLHAParameters')
    )
)


process.load("RecoJets.Configuration.GenJetParticles_cff")
#process.genParticlesForJets.ignoreParticleIDs.extend(cms.vuint32(5000039))
process.load("RecoJets.JetProducers.ak5GenJets_cfi")


process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
#	 src = cms.InputTag("ak5GenJets"),
     maxEventsToPrint = cms.untracked.int32(1)
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



process.genParticlesClone1 = cms.EDFilter("CandViewShallowCloneProducer",
							 src = cms.InputTag("genParticles"),
    cut = cms.string("pt > 10 & abs( eta ) < 2.5 & status = 1 & ( abs(pdgId)=11 | abs(pdgId)=13 )")							 
							 )


process.rawmuons = cms.EDFilter("PdgIdAndStatusCandSelector",
						   src = cms.InputTag("genParticlesClone1"),
						   pdgId = cms.vint32( 13 ),
						   status = cms.vint32( 1 )							 
)


process.rawelectrons = cms.EDFilter("PdgIdAndStatusCandSelector",
						   src = cms.InputTag("genParticlesClone1"),
						   pdgId = cms.vint32( 11 ),
						   status = cms.vint32( 1 )							 
)

process.jets = cms.EDProducer("GenJetShallowCloneProducer",
							  src = cms.InputTag("ak5GenJets")
							  )

process.selectedMuons = cms.EDFilter("CandSelector",
    src = cms.InputTag("rawmuons"),
    cut = cms.string("pt > 10 & abs( eta ) < 2.4")
  )

process.selectedElectrons = cms.EDFilter("CandSelector",
    src = cms.InputTag("rawelectrons"),
    cut = cms.string("pt > 15 & abs( eta ) < 2.5")
  )

# should require e/mu to be isolated

process.selectedJets = cms.EDFilter("CandSelector",
    src = cms.InputTag("jets"),
    cut = cms.string("pt > 50 & abs( eta ) < 2.5")
  )

process.HTvector = cms.EDProducer("CompositeProducer",
										 dauSrc = cms.InputTag("selectedJets"),
										 )



process.countFilter = cms.EDFilter("CandCountFilter",
								   src = cms.InputTag("selectedJets"),
								   minNumber = cms.uint32(3)
								   )


process.electronVeto = cms.EDFilter("CandCountFilter",
								   src = cms.InputTag("selectedElectrons"),
								   minNumber = cms.uint32(1)
								   )


process.muonVeto = cms.EDFilter("CandCountFilter",
								   src = cms.InputTag("selectedMuons"),
								   minNumber = cms.uint32(1)
								   )


process.HT = cms.EDProducer("HTProducer",
							JetCollection = cms.InputTag("ak5GenJets"),
							MinJetPt = cms.double(50.0),
							MaxJetEta = cms.double(2.5)
							)

process.MHT = cms.EDProducer("MHTProducer",
							JetCollection = cms.InputTag("ak5GenJets"),
							MinJetPt = cms.double(50.0),
							MaxJetEta = cms.double(2.5)
							)


### HT > 300 GeV from HTProducer

process.htSelect = cms.EDFilter("HTFilter",
    HTSource = cms.InputTag("HT"),
    MinHT = cms.double(300.)
  )
### MHT > 150 GeV for MHTProducer
process.mhtSelect = cms.EDFilter("MHTFilter",
    MHTSource = cms.InputTag("MHT"),
    MinMHT = cms.double(150.)
  )



### deltaR --> deltaPhi -->  mht * jet0 > 0.5 *jet1 > 0.5 *jet2>0.3
process.dphiSelect = cms.EDFilter("JetMHTDPhiFilter",
								  MHTSource = cms.InputTag("MHT"),
								  JetSource = cms.InputTag("ak5GenJets")
								  )



process.missingPt= cms.EDAnalyzer("CandViewHistoAnalyzer",
#							src = cms.InputTag("ak5GenJetsClone"),
							src = cms.InputTag("MHT"),							   
	  # weights = cms.untracked.InputTag("myProducerLabel"),							   
 histograms = cms.VPSet(
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(1),
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(1000.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("missing_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    )
		)
)
		
process.sumHt= cms.EDAnalyzer("CandViewHistoAnalyzer",
#							src = cms.InputTag("ak5GenJetsClone"),
							src = cms.InputTag("HTvector"),							   
	  # weights = cms.untracked.InputTag("myProducerLabel"),							   
 histograms = cms.VPSet(
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(1),
	    min = cms.untracked.double(0.0),
	    max = cms.untracked.double(1000.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("sum HT"),
	    description = cms.untracked.string("HT [GeV/c]"),
	    plotquantity = cms.untracked.string("energy")
	    )
		)
)


process.jetsPt= cms.EDAnalyzer("CandViewHistoAnalyzer",
#							src = cms.InputTag("ak5GenJetsClone"),
							src = cms.InputTag("ak5GenJets"),							   
	  # weights = cms.untracked.InputTag("myProducerLabel"),							   
 histograms = cms.VPSet(
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
	    min = cms.untracked.double(20.0),
	    max = cms.untracked.double(500.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("jet_pT"),
	    description = cms.untracked.string("pT [GeV/c]"),
	    plotquantity = cms.untracked.string("pt")
	    ),
		cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
		min = cms.untracked.double(0.0),
	    max = cms.untracked.double(100.0),
	    nbins = cms.untracked.int32(50),
	    name = cms.untracked.string("jet_mass"),
	    description = cms.untracked.string("mass [GeV/c^2]"),
	    plotquantity = cms.untracked.string("mass")
	    ),
	    cms.PSet(
            itemsToPlot = cms.untracked.int32(5),
	    min = cms.untracked.double(-5.0),
	    max = cms.untracked.double(5.0),
	    nbins = cms.untracked.int32(100),
	    name = cms.untracked.string("jet_rap"),
	    description = cms.untracked.string("rapidity"),
	    plotquantity = cms.untracked.string("rapidity")
	    )						
		)
)




process.pp = cms.Path(process.generator*process.genParticles*
 	process.genParticlesForJets
					 *process.ak5GenJets

*process.genParticlesClone1 *

process.rawmuons *

process.rawelectrons *

process.jets *

#*process.myProducerLabel

process.jetsPt

#*process.extraPlots
					 )



process.schedule = cms.Schedule(process.pp)

