import FWCore.ParameterSet.Config as cms

generator = cms.EDFilter("Pythia8GeneratorFilter",
        comEnergy = cms.double(7000.0),
        filterEfficiency = cms.untracked.double(1),
        maxEventsToPrint = cms.untracked.int32(1),
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        PythiaParameters = cms.PSet(
                processParameters = cms.vstring(
                        'Main:timesAllowErrors = 10000',
                        'ParticleDecays:limitTau0 = on',
                        'ParticleDecays:tauMax = 10',
#                        'Tune:ee 3',
#                        'Tune:pp 5',
                        'WeakSingleBoson:ffbar2W = on',
                        '24:onMode = off',
                        '24:onIfAny = 11 12 13 14',
						'PDF:useHard = on',
						'PDF:pHardSet = 9'
#                        '24:mMin = 500.',
                ),
                parameterSets = cms.vstring('processParameters')
        )
)

