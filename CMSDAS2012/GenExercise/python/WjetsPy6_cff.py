import FWCore.ParameterSet.Config as cms

from Configuration.Generator.PythiaUESettings_cfi import *

#from GeneratorInterface.ExternalDecays.TauolaSettings_cff import *
generator = cms.EDFilter("Pythia6GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(5),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(7000.0),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        WjetsParameters = cms.vstring('MSEL=0',
			'MSUB(2)=1',
			'24:ALLOFF',
			'24:ONIFANY 11 12 13 14'),
        parameterSets = cms.vstring('pythiaUESettings', 
            'WjetsParameters')
    )
)
