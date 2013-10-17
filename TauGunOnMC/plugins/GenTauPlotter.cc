
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1F.h"
#include "TH2F.h"


class GenTauPlotter : public edm::EDAnalyzer {

  public:

    explicit GenTauPlotter(const edm::ParameterSet & iConfig);
    ~GenTauPlotter();

  private:

    virtual void analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup);
    void findDaughters(std::vector<const reco::GenParticle *> & tauparts, const reco::GenParticle * particle);

    edm::Service<TFileService> fs;
    edm::InputTag genSrc_[2];
    TH1F * h_tot_npart[2],      * h_chd_npart[2],      * h_ntr_npart[2];
    TH1F * h_tot_vispt[2],      * h_chd_vispt[2],      * h_ntr_vispt[2];
    TH1F * h_tot_leadpt[2],     * h_chd_leadpt[2],     * h_ntr_leadpt[2];
    TH1F * h_tot_visptfrac[2],  * h_chd_visptfrac[2],  * h_ntr_visptfrac[2];
    TH1F * h_tot_leadptfrac[2], * h_chd_leadptfrac[2], * h_ntr_leadptfrac[2];

};


GenTauPlotter::GenTauPlotter(const edm::ParameterSet& iConfig) {
  genSrc_[0]      = iConfig.getParameter<edm::InputTag>("GenSrc1");
  genSrc_[1]      = iConfig.getParameter<edm::InputTag>("GenSrc2");
  h_tot_npart[0]      = fs->make<TH1F>("h1_tot_npart",      "Nr particles",                  20, 0,  20);
  h_chd_npart[0]      = fs->make<TH1F>("h1_chd_npart",      "Nr particles",                  20, 0,  20);
  h_ntr_npart[0]      = fs->make<TH1F>("h1_ntr_npart",      "Nr particles",                  20, 0,  20);
  h_tot_npart[1]      = fs->make<TH1F>("h2_tot_npart",      "Nr particles",                  20, 0,  20);
  h_chd_npart[1]      = fs->make<TH1F>("h2_chd_npart",      "Nr particles",                  20, 0,  20);
  h_ntr_npart[1]      = fs->make<TH1F>("h2_ntr_npart",      "Nr particles",                  20, 0,  20);
  h_tot_vispt[0]      = fs->make<TH1F>("h1_tot_vispt",      "Visible tau pT",               100, 0, 100);
  h_chd_vispt[0]      = fs->make<TH1F>("h1_chd_vispt",      "Visible tau pT",               100, 0, 100);
  h_ntr_vispt[0]      = fs->make<TH1F>("h1_ntr_vispt",      "Visible tau pT",               100, 0, 100);
  h_tot_vispt[1]      = fs->make<TH1F>("h2_tot_vispt",      "Visible tau pT",               100, 0, 100);
  h_chd_vispt[1]      = fs->make<TH1F>("h2_chd_vispt",      "Visible tau pT",               100, 0, 100);
  h_ntr_vispt[1]      = fs->make<TH1F>("h2_ntr_vispt",      "Visible tau pT",               100, 0, 100);
  h_tot_leadpt[0]     = fs->make<TH1F>("h1_tot_leadpt",     "Leading particle pT",          100, 0, 100);
  h_chd_leadpt[0]     = fs->make<TH1F>("h1_chd_leadpt",     "Leading particle pT",          100, 0, 100);
  h_ntr_leadpt[0]     = fs->make<TH1F>("h1_ntr_leadpt",     "Leading particle pT",          100, 0, 100);
  h_tot_leadpt[1]     = fs->make<TH1F>("h2_tot_leadpt",     "Leading particle pT",          100, 0, 100);
  h_chd_leadpt[1]     = fs->make<TH1F>("h2_chd_leadpt",     "Leading particle pT",          100, 0, 100);
  h_ntr_leadpt[1]     = fs->make<TH1F>("h2_ntr_leadpt",     "Leading particle pT",          100, 0, 100);
  h_tot_visptfrac[0]  = fs->make<TH1F>("h1_tot_visptfrac",  "Visible tau pT fraction",      100, 0,   1);
  h_chd_visptfrac[0]  = fs->make<TH1F>("h1_chd_visptfrac",  "Visible tau pT fraction",      100, 0,   1);
  h_ntr_visptfrac[0]  = fs->make<TH1F>("h1_ntr_visptfrac",  "Visible tau pT fraction",      100, 0,   1);
  h_tot_visptfrac[1]  = fs->make<TH1F>("h2_tot_visptfrac",  "Visible tau pT fraction",      100, 0,   1);
  h_chd_visptfrac[1]  = fs->make<TH1F>("h2_chd_visptfrac",  "Visible tau pT fraction",      100, 0,   1);
  h_ntr_visptfrac[1]  = fs->make<TH1F>("h2_ntr_visptfrac",  "Visible tau pT fraction",      100, 0,   1);
  h_tot_leadptfrac[0] = fs->make<TH1F>("h1_tot_leadptfrac", "Leading particle pT fraction", 100, 0,   1);
  h_chd_leadptfrac[0] = fs->make<TH1F>("h1_chd_leadptfrac", "Leading particle pT fraction", 100, 0,   1);
  h_ntr_leadptfrac[0] = fs->make<TH1F>("h1_ntr_leadptfrac", "Leading particle pT fraction", 100, 0,   1);
  h_tot_leadptfrac[1] = fs->make<TH1F>("h2_tot_leadptfrac", "Leading particle pT fraction", 100, 0,   1);
  h_chd_leadptfrac[1] = fs->make<TH1F>("h2_chd_leadptfrac", "Leading particle pT fraction", 100, 0,   1);
  h_ntr_leadptfrac[1] = fs->make<TH1F>("h2_ntr_leadptfrac", "Leading particle pT fraction", 100, 0,   1);
}


GenTauPlotter::~GenTauPlotter() {
}


void GenTauPlotter::analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup) {

  edm::Handle<std::vector<reco::GenParticle> > genparts[2];
  std::vector<const reco::GenParticle *> tauparts[2];

  for (unsigned int k = 0; k < 2; ++k) {

    iEvent.getByLabel(genSrc_[k], genparts[k]);

    float pt = 0;
    for (unsigned int i = 0; i < genparts[k]->size(); ++i) {
      const reco::GenParticle * particle = &(*genparts[k])[i];
      if (particle->status() == (k==0?3:2) && std::abs(particle->pdgId()) == 15) {
        pt = particle->pt();
        findDaughters(tauparts[k], particle);
        break;
      }
    }

    float npart_chd = 0, npart_ntr = 0;
    float vispt_chd = 0, vispt_ntr = 0;
    float leadpt_chd = 0, leadpt_ntr = 0, leadpt_all = 0;
    for (unsigned int i = 0; i < tauparts[k].size(); ++i) {
      if (fabs(tauparts[k][i]->pdgId())!=12 &&
          fabs(tauparts[k][i]->pdgId())!=14 &&
          fabs(tauparts[k][i]->pdgId())!=16) {
        if (tauparts[k][i]->charge() == 0) {
          ++npart_ntr;
          vispt_ntr += tauparts[k][i]->pt();
          if (tauparts[k][i]->pt() > leadpt_ntr) leadpt_ntr = tauparts[k][i]->pt();
        } else {
          ++npart_chd;
          vispt_chd += tauparts[k][i]->pt();
          if (tauparts[k][i]->pt() > leadpt_chd) leadpt_chd = tauparts[k][i]->pt();
        }
        if (tauparts[k][i]->pt() > leadpt_all) leadpt_all = tauparts[k][i]->pt();
      }
    }

    h_chd_npart[k]->Fill(npart_chd);
    h_ntr_npart[k]->Fill(npart_ntr);
    h_tot_npart[k]->Fill(npart_chd+npart_ntr);
    h_chd_vispt[k]->Fill(vispt_chd);
    h_ntr_vispt[k]->Fill(vispt_ntr);
    h_tot_vispt[k]->Fill(vispt_chd+vispt_ntr);
    h_chd_leadpt[k]->Fill(leadpt_chd);
    h_ntr_leadpt[k]->Fill(leadpt_ntr);
    h_tot_leadpt[k]->Fill(leadpt_all);
    h_chd_visptfrac[k]->Fill(vispt_chd/pt);
    h_ntr_visptfrac[k]->Fill(vispt_ntr/pt);
    h_tot_visptfrac[k]->Fill((vispt_chd+vispt_ntr)/pt);
    h_chd_leadptfrac[k]->Fill(leadpt_chd/pt);
    h_ntr_leadptfrac[k]->Fill(leadpt_ntr/pt);
    h_tot_leadptfrac[k]->Fill(leadpt_all/pt);

  }

}


void GenTauPlotter::findDaughters(std::vector<const reco::GenParticle *> & tauparts, const reco::GenParticle * particle) {
  for (unsigned int i = 0; i < particle->numberOfDaughters(); ++i) {
    const reco::GenParticle * dau = dynamic_cast<const reco::GenParticle *>(particle->daughter(i));
    dau->numberOfDaughters() == 0 ?  tauparts.push_back(dau) : findDaughters(tauparts, dau);
  }
}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(GenTauPlotter);
