
import FWCore.ParameterSet.Config as cms

tauGunMerge = cms.EDProducer(
  "TauGunMerger",
  pfsrc1 = cms.InputTag("tauGunSplit:pfNoMu"),
  pfsrc2 = cms.InputTag("particleFlow"), # will take the latest one, from the taus
  trsrc1 = cms.InputTag("tauGunSplit:tracksNoMu"),
  trsrc2 = cms.InputTag("generalTracks"), # will take the latest one, from the taus
  vtxsrc = cms.InputTag("offlinePrimaryVertices::RECO"), # important to take the ones from RECO!!!
)
