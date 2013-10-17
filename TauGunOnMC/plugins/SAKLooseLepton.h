#ifndef SAKLooseLepton_h
#define SAKLooseLepton_h

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "TMath.h"

bool isLooseElectron(const reco::GsfElectron & electron, const math::XYZPoint & primaryVertex, edm::Handle<reco::PFCandidateCollection> pfCandidates);
bool isLooseMuon(const reco::Muon & muon, const math::XYZPoint & primaryVertex, edm::Handle<reco::PFCandidateCollection> pfCandidates);

bool passCut(double parameter, double variable, bool discardAbove, int numBins, const double* parameterBins, const double* variableCuts);

/**
  If the directional parameter is set, computes directional isolation, i.e. an
  (angular-)disperson weighted sum of pT of the provided isoParticles. Otherwise
  computes a simple scalar sum of isoParticles. In both cases the pT of the
  particles involved can be weighted or not by a gaussian fall-off instead of
  a strict use-it-or-not cone.
  @note   The probe particle is always omitted from the considered isoParticles
          (if they are from the same collection, of course).
*/
template<typename Particle, typename IsoParticle>
static double customIsolation(const Particle& particle, const edm::Handle<std::vector<IsoParticle> >& isoParticles, double coneDR, bool directional, bool falloff, reco::PFCandidate::ParticleType lepton)
{

  //if (lepton == reco::PFCandidate::e) std::cout << "PARTICLE " << particle.gsfTrack().isNonnull() << " " << particle.gsfTrack().id() << " " << particle.gsfTrack().key() << std::endl;

  const double                              maxDR         = ( falloff ? 5*coneDR : coneDR );
  double                                    isoSum        = 0;
  math::XYZVector              isoAngleSum;
  std::vector<math::XYZVector> coneParticles;
  bool matched = false;
  for (unsigned int iPtcl = 0; iPtcl < isoParticles->size(); ++iPtcl) {
    if (lepton == reco::PFCandidate::mu && (*isoParticles)[iPtcl].muonRef().isNonnull() && (*isoParticles)[iPtcl].trackRef() == particle.track()) {
      matched = true; continue; }
    if (lepton == reco::PFCandidate::e  && (*isoParticles)[iPtcl].gsfTrackRef().isNonnull() && (*isoParticles)[iPtcl].gsfTrackRef() == particle.gsfTrack()) {
      matched = true; continue; }
    const IsoParticle&                  isoParticle   = (*isoParticles)[iPtcl];
    const double                        dR            = reco::deltaR(isoParticle, particle);
    if (dR > maxDR)                                                                     continue;
    if (isoParticle.particleId() == reco::PFCandidate::gamma && isoParticle.pt() < 0.5) continue;
    if (isoParticle.particleId() == reco::PFCandidate::h0    && isoParticle.pt() < 0.5) continue;
    const double                        weight        = falloff
                                                      ? TMath::Gaus(dR, 0, coneDR, true)
                                                      : 1
                                                      ;

    //.........................................................................
    if (directional) {
      math::XYZVector      transverse( isoParticle.eta() - particle.eta()
                                     , reco::deltaPhi(isoParticle.phi(), particle.phi())
                                     , 0);
      transverse                       *= weight * isoParticle.pt() / transverse.rho();
      if (transverse.rho() > 0) {
        isoAngleSum                    += transverse;
        coneParticles.push_back(transverse);
      } else if (lepton == reco::PFCandidate::e) std::cout << "ZERO! " << (*isoParticles)[iPtcl].muonRef().isNonnull() << " "
                                                           << (*isoParticles)[iPtcl].gsfTrackRef().id() << " " << particle.gsfTrack().id()
                                                           << " " << (*isoParticles)[iPtcl].gsfTrackRef().key() << " " << particle.gsfTrack().key() << std::endl;
    }
    //.........................................................................
    else {
      isoSum                           += weight * isoParticle.pt();
    }
  } // end loop over PF candidates

  if (!matched) std::cout << "AAAH a non-matched lepton! " << (int) (lepton == reco::PFCandidate::mu) << " " << (int) (lepton == reco::PFCandidate::e) << " " << isoSum << " " << particle.pt() << std::endl;

  if (directional) {
    double                              directionalPT = 0;
    for (unsigned int iPtcl = 0; iPtcl < coneParticles.size(); ++iPtcl)
      directionalPT                    += pow(TMath::ACos( coneParticles[iPtcl].Dot(isoAngleSum) / coneParticles[iPtcl].rho() / isoAngleSum.rho() ),2)
                                        * coneParticles[iPtcl].rho()
                                        ;
    return directionalPT;
  }
  return isoSum;

}

#endif

