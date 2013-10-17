# Auto generated configuration file
# using: 
# Revision: 1.303 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: GEN-fragment --step GEN,FASTSIM,HLT:GRun,VALIDATION:validation_prod,DQM:DQMOfflinePOGMC --beamspot Realistic7TeV2011Collision --conditions START42_V11::All --pileup FlatDist10_2011EarlyData_50ns --geometry DB --datamix NODATAMIXER --eventcontent AODSIM,DQM --datatier AODSIM,DQM
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.PythiaUESettings_cfi import *

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_FlatDist10_2011EarlyData_50ns_cff')
process.load('FastSimulation.Configuration.Geometries_START_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.HLT_GRun_cff')
process.load('FastSimulation.Configuration.Validation_cff')
process.load('DQMOffline.Configuration.DQMOfflineMC_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(100)
)

# Input source
#process.source = cms.Source(
#   "LHESource",
#   fileNames = cms.untracked.vstring('file:ttbar.lhe'),
#   skipEvents = cms.untracked.uint32(0)
#)

process.source = cms.Source("PoolSource",
fileNames=cms.untracked.vstring('/store/generator/Summer11/mSUGRA_m0-20to2000_m12-20to760_tanb-10andA0-0_7TeV-Pythia6Z/GEN/START42_V11-v2/0000/2EA554F5-AEA1-E011-B1DA-003048CFB394.root')
)


process.generator = cms.EDFilter("Pythia6HadronizerFilter",
   pythiaHepMCVerbosity = cms.untracked.bool(False),
   maxEventsToPrint = cms.untracked.int32(1),
   pythiaPylistVerbosity = cms.untracked.int32(1),
   comEnergy = cms.double(7000.0),
PythiaParameters = cms.PSet(
       pythiaUESettingsBlock,
       processParameters = cms.vstring('MSEL=0         ! User defined processes',
                       'PMAS(5,1)=4.4   ! b quark mass',
                       'PMAS(6,1)=172.4 ! t quark mass',
                       'MSTJ(1)=1       ! Fragmentation/hadronization on or off',
 #                      'IMSS(1)=1',
                       'MSTP(61)=1      ! Parton showering on or off'),
       # This is a vector of ParameterSet names to be read, in this order
       parameterSets = cms.vstring('pythiaUESettings',
           'processParameters')
   )
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
   version = cms.untracked.string('$Revision: 1.1 $'),
   annotation = cms.untracked.string('GEN-fragment nevts:1'),
   name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
   eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
   outputCommands = process.AODSIMEventContent.outputCommands,
   fileName = cms.untracked.string('GEN-fragment_GEN_FASTSIM_HLT_VALIDATION_DQM_PU.root'),
   dataset = cms.untracked.PSet(
       filterName = cms.untracked.string(''),
       dataTier = cms.untracked.string('AODSIM')
   ),
   SelectEvents = cms.untracked.PSet(
       SelectEvents = cms.vstring('generation_step')
   )
)

process.DQMoutput = cms.OutputModule("PoolOutputModule",
   splitLevel = cms.untracked.int32(0),
   outputCommands = process.DQMEventContent.outputCommands,
   fileName = cms.untracked.string('GEN-fragment_GEN_FASTSIM_HLT_VALIDATION_DQM_PU_inDQM.root'),
   dataset = cms.untracked.PSet(
       filterName = cms.untracked.string(''),
       dataTier = cms.untracked.string('DQM')
   ),
   SelectEvents = cms.untracked.PSet(
       SelectEvents = cms.vstring('generation_step')
   )
)

# Additional output definition

# Other statements
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic7TeV2011CollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic7TeV2011CollisionVtxSmearingParameters
process.mix.playback = True
process.GlobalTag.globaltag = 'START42_V11::All'

# Path and EndPath definitions
#process.generation_step = cms.Path(process.pgen_genonly)
process.generation_step = cms.Path(process.generator)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.validation_step = cms.EndPath(process.validation_prod)
process.dqmoffline_step = cms.EndPath(process.DQMOfflinePOGMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.validation_step,process.dqmoffline_step,process.endjob_step,process.AODSIMoutput_step,process.DQMoutput_step])

