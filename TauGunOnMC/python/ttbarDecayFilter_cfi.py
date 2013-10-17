
import FWCore.ParameterSet.Config as cms

#  Encoding of the integer vector, interpreted as bool:
#    0 : exactly 1 PromptE
#    1 : exactly 1 PromptM
#    2 : exactly 1 TauE
#    3 : exactly 1 TauM
#    4 : exactly 1 TauH
#    5 : exactly 2 PromptE
#    6 : exactly 1 PromptE + exactly 1 PromptM
#    7 : exactly 1 PromptE + exactly 1 TauE
#    8 : exactly 1 PromptE + exactly 1 TauM
#    9 : exactly 1 PromptE + exactly 1 TauH
#    10: exactly 2 PromptM
#    11: exactly 1 PromptM + exactly 1 TauE
#    12: exactly 1 PromptM + exactly 1 TauM
#    13: exactly 1 PromptM + exactly 1 TauH
#    14: exactly 2 TauE
#    15: exactly 1 TauE + exactly 1 TauM
#    16: exactly 1 TauE + exactly 1 TauH
#    17: exactly 2 TauM
#    18: exactly 1 TauM + exactly 1 TauH
#    19: exactly 2 TauH

# filter to select electron final states, without muons
eleOnlySel = cms.EDFilter(
  "TtbarDecayFilter",
  GenParticleSrc = cms.InputTag('genParticles'),
  BoolSrc = cms.vint32(1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0)
)

# filter to select final states with both muons and electrons
eleMuSel = cms.EDFilter(
  "TtbarDecayFilter",
  GenParticleSrc = cms.InputTag('genParticles'),
  BoolSrc = cms.vint32(0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0)
)

# filter to select muon final states, without electrons
muOnlySel = cms.EDFilter(
  "TtbarDecayFilter",
  GenParticleSrc = cms.InputTag('genParticles'),
  BoolSrc = cms.vint32(0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0)
)

# filter to select final states with hadronic taus
hadTauSel = cms.EDFilter(
  "TtbarDecayFilter",
  GenParticleSrc = cms.InputTag('genParticles'),
  BoolSrc = cms.vint32(0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
)
