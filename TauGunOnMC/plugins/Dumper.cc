
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"


class Dumper : public edm::EDAnalyzer {

  public:

    explicit Dumper(const edm::ParameterSet & iConfig);
    ~Dumper();

  private:

    virtual void analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup);

    edm::InputTag pfJetSource_;
    edm::InputTag mhtSource_;
    edm::InputTag htSource_;
    std::string header_;

};


Dumper::Dumper(const edm::ParameterSet& iConfig) {
  pfJetSource_ = iConfig.getParameter<edm::InputTag>("PFJetSource");
  mhtSource_ = iConfig.getParameter<edm::InputTag>("MHTSource");
  htSource_  = iConfig.getParameter<edm::InputTag>("HTSource");
  header_  = iConfig.getParameter<std::string>("Header");
}


Dumper::~Dumper() {
}


void Dumper::analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup) {

  std::cout << "##### " << header_.data() << " ##########" << std::endl;

  std::cout << "R:L:E " << iEvent.run() << ":" << iEvent.luminosityBlock() << ":" << iEvent.id().event() << std::endl;

  edm::Handle<edm::View<reco::MET> > mht;
  iEvent.getByLabel(mhtSource_, mht);
  if (mht.isValid() && !mht.failedToGet())
    std::cout << "MHT : " << (*mht)[0].pt() << std::endl;

  edm::Handle<edm::View<reco::MET> > ht;
  iEvent.getByLabel(htSource_, ht);
  if (ht.isValid() && !ht.failedToGet()) 
    std::cout << "HT  : " << (*ht)[0].sumEt() << std::endl;

  edm::Handle<reco::PFJetCollection> pfJets;
  iEvent.getByLabel(pfJetSource_, pfJets);
  int nj = 0;
  for ( reco::PFJetCollection::const_iterator pfJet = pfJets->begin(); pfJet != pfJets->end(); pfJet++ ) {
    if (pfJet->pt() < 30) continue;
    std::cout << "Jet " << ++nj
              << " E/pt/eta/phi : " << pfJet->energy()
              << " " << pfJet->pt() 
              << " " << pfJet->eta()
              << " " << pfJet->phi() << std::endl;
    std::vector<reco::PFCandidatePtr> constituents = pfJet->getPFConstituents();
    for ( unsigned ic = 0; ic < constituents.size() ; ++ic ) { 
      const reco::PFCandidate pfc = *(constituents[ic]);
      std::cout << pfc << std::endl;
    } 
  }

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(Dumper);
