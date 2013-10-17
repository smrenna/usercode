
// Author: S. Lowette

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"


class AnyCandToCaloJetProducer: public edm::EDProducer {

  public:

    explicit AnyCandToCaloJetProducer(const edm::ParameterSet&);
    ~AnyCandToCaloJetProducer();

    virtual void produce(edm::Event&, const edm::EventSetup&);

  private:

    edm::InputTag candSrc_;

};


AnyCandToCaloJetProducer::AnyCandToCaloJetProducer(const edm::ParameterSet& iConfig) {
  candSrc_ = iConfig.getParameter<edm::InputTag>("Source");
  produces<reco::CaloJetCollection>();
}

AnyCandToCaloJetProducer::~AnyCandToCaloJetProducer() {
}

void AnyCandToCaloJetProducer::produce(edm::Event& iEvent, const edm::EventSetup& iES) {

  std::auto_ptr<reco::CaloJetCollection> jets(new reco::CaloJetCollection());

  edm::Handle<edm::View<reco::Candidate> > cands;
  if (iEvent.getByLabel( candSrc_, cands )) {
    for(edm::View<reco::Candidate>::const_iterator i = cands->begin(); i != cands->end(); i++ ) {
      reco::CaloJet jet(i->p4(), i->vertex(), reco::CaloJet::Specific());
      jets->push_back(jet);
    }
  }

  iEvent.put(jets);

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(AnyCandToCaloJetProducer);
