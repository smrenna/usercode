
// Author: S. Lowette

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/CaloMETFwd.h"
#include "DataFormats/METReco/interface/CaloMET.h"


class AnyCandToCaloMETProducer: public edm::EDProducer {

  public:

    explicit AnyCandToCaloMETProducer(const edm::ParameterSet&);
    ~AnyCandToCaloMETProducer();

    virtual void produce(edm::Event&, const edm::EventSetup&);

  private:

    edm::InputTag candSrc_;

};


AnyCandToCaloMETProducer::AnyCandToCaloMETProducer(const edm::ParameterSet& iConfig) {
  candSrc_ = iConfig.getParameter<edm::InputTag>("Source");
  produces<reco::CaloMETCollection>();
}


AnyCandToCaloMETProducer::~AnyCandToCaloMETProducer() {
}


void AnyCandToCaloMETProducer::produce(edm::Event& iEvent, const edm::EventSetup& iES) {

  std::auto_ptr<reco::CaloMETCollection> newmet(new reco::CaloMETCollection());

  edm::Handle<edm::View<reco::Candidate> > cands;
  if (iEvent.getByLabel( candSrc_, cands )) {
    if (cands->size()!=0) {
      newmet->push_back(reco::CaloMET(SpecificCaloMETData(), 0, (*cands)[0].p4(), reco::MET::Point()));
    } else {
      newmet->push_back(reco::CaloMET(SpecificCaloMETData(), 0, reco::MET::LorentzVector(), reco::MET::Point()));
    }
  }

  iEvent.put(newmet);

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(AnyCandToCaloMETProducer);
