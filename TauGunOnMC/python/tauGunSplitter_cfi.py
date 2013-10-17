
import FWCore.ParameterSet.Config as cms

tauGunSplit = cms.EDProducer(
  "TauGunSplitter",
  PFSource = cms.InputTag("pfNoPileUpPFchs"),
  TrackSource = cms.InputTag("generalTracks"),
  VertexSource = cms.InputTag("offlinePrimaryVertices"),
)

# next you can count the muons for instance with the following:
#
# process.countPFMu = cms.EDFilter(
#   "CandViewCountFilter",
#   src = cms.InputTag("tauGunSplit:pfMu"),
#   minNumber = cms.uint32(1),
#   maxNumber = cms.uint32(1)
# )
