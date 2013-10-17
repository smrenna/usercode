
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

/*

  Filter on ttbar decay modes based on an .OR. of many boolean switches

  Encoding of the integer vector, interpreted as bool:
    0 : exactly 1 PromptE
    1 : exactly 1 PromptM
    2 : exactly 1 TauE
    3 : exactly 1 TauM
    4 : exactly 1 TauH
    5 : exactly 2 PromptE
    6 : exactly 1 PromptE + exactly 1 PromptM
    7 : exactly 1 PromptE + exactly 1 TauE
    8 : exactly 1 PromptE + exactly 1 TauM
    9 : exactly 1 PromptE + exactly 1 TauH
    10: exactly 2 PromptM
    11: exactly 1 PromptM + exactly 1 TauE
    12: exactly 1 PromptM + exactly 1 TauM
    13: exactly 1 PromptM + exactly 1 TauH
    14: exactly 2 TauE
    15: exactly 1 TauE + exactly 1 TauM
    16: exactly 1 TauE + exactly 1 TauH
    17: exactly 2 TauM
    18: exactly 1 TauM + exactly 1 TauH
    19: exactly 2 TauH

*/

class TtbarDecayFilter : public edm::EDFilter {

  public:

    explicit TtbarDecayFilter(const edm::ParameterSet & iConfig);
    ~TtbarDecayFilter() {}

  private:

    virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);

    bool isOutgoing(const reco::GenParticle * particle);
    void checkDecayProducts(const reco::Candidate * particle, int & numElectrons, int & numMuons);
    
    edm::InputTag genSrc_;
    std::vector<int> boolSrc_;

    enum ParticleID { p_eminus = 11, p_nu_e, p_muminus, p_nu_mu, p_tauminus, p_nu_tau };

};


TtbarDecayFilter::TtbarDecayFilter(const edm::ParameterSet & iConfig) {
  genSrc_  = iConfig.getParameter<edm::InputTag>("GenParticleSrc");
  boolSrc_ = iConfig.getParameter<std::vector<int> >("BoolSrc");
  if (boolSrc_.size() < 20) throw edm::Exception(edm::errors::Configuration) << "Incorrect bool vector for filter switches";
}


bool TtbarDecayFilter::filter(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  edm::Handle<std::vector<reco::GenParticle> > genparts;
  iEvent.getByLabel(genSrc_, genparts);

  int nPromptE       = 0;
  int nPromptMu      = 0;
  int nPromptTauToE  = 0;
  int nPromptTauToMu = 0;
  int nPromptTauHad  = 0;

  for (unsigned int iPtcl = 6; iPtcl < genparts->size(); ++iPtcl) {
    const reco::GenParticle & particle = (*genparts)[iPtcl];
    if (particle.status() != 3) break;
    if (!isOutgoing(&particle)) continue;
    int numElectrons = 0, numMuons = 0;
    switch (std::abs(particle.pdgId())) {
      case p_eminus:   ++nPromptE;   break;
      case p_muminus:  ++nPromptMu;  break;
      case p_tauminus: checkDecayProducts(&particle, numElectrons, numMuons);
                       if      (numMuons)     ++nPromptTauToMu;
                       else if (numElectrons) ++nPromptTauToE;
                       else                   ++nPromptTauHad;
                       break;
      default:         break;
    }
  } // end loop over genParticles

  bool result = false;
  if (boolSrc_[0])  result = result || (nPromptE == 1 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[1])  result = result || (nPromptE == 0 && nPromptMu == 1 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[2])  result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 1 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[3])  result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 1 && nPromptTauHad == 0);
  if (boolSrc_[4])  result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 1);
  if (boolSrc_[5])  result = result || (nPromptE == 2 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[6])  result = result || (nPromptE == 1 && nPromptMu == 1 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[7])  result = result || (nPromptE == 1 && nPromptMu == 0 && nPromptTauToE == 1 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[8])  result = result || (nPromptE == 1 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 1 && nPromptTauHad == 0);
  if (boolSrc_[9])  result = result || (nPromptE == 1 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 1);
  if (boolSrc_[10]) result = result || (nPromptE == 0 && nPromptMu == 2 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[11]) result = result || (nPromptE == 0 && nPromptMu == 1 && nPromptTauToE == 1 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[12]) result = result || (nPromptE == 0 && nPromptMu == 1 && nPromptTauToE == 0 && nPromptTauToMu == 1 && nPromptTauHad == 0);
  if (boolSrc_[13]) result = result || (nPromptE == 0 && nPromptMu == 1 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 1);
  if (boolSrc_[14]) result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 2 && nPromptTauToMu == 0 && nPromptTauHad == 0);
  if (boolSrc_[15]) result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 1 && nPromptTauToMu == 1 && nPromptTauHad == 0);
  if (boolSrc_[16]) result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 1 && nPromptTauToMu == 0 && nPromptTauHad == 1);
  if (boolSrc_[17]) result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 2 && nPromptTauHad == 0);
  if (boolSrc_[18]) result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 1 && nPromptTauHad == 1);
  if (boolSrc_[19]) result = result || (nPromptE == 0 && nPromptMu == 0 && nPromptTauToE == 0 && nPromptTauToMu == 0 && nPromptTauHad == 2);
  return result;

}


bool TtbarDecayFilter::isOutgoing(const reco::GenParticle * particle) {
  if (particle->status() != 3) return false;
  for (unsigned int iDau = 0; iDau < particle->numberOfDaughters(); ++iDau) {
    if (particle->daughter(iDau)->status() == 3) return false;
  }
  return true;
}


void TtbarDecayFilter::checkDecayProducts(const reco::Candidate * particle, int & numElectrons, int & numMuons) {
  if (particle->numberOfDaughters()) {
    for (unsigned int iDau = 0; iDau < particle->numberOfDaughters(); ++iDau)
      checkDecayProducts(particle->daughter(iDau), numElectrons, numMuons);
  }
  else if (std::abs(particle->pdgId()) == p_eminus) {
    ++numElectrons;
  }
  else if (std::abs(particle->pdgId()) == p_muminus) {
    ++numMuons;
  }
}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(TtbarDecayFilter);
