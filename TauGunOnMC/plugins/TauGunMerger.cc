
#include <memory>
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"


class TauGunMerger : public edm::EDProducer {

  public:

    explicit TauGunMerger(const edm::ParameterSet & iConfig);
    ~TauGunMerger();

    virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);

  private:

    edm::InputTag pfSrc1_, pfSrc2_, trSrc1_, trSrc2_, vtxSrc_;

};


TauGunMerger::TauGunMerger(const edm::ParameterSet & iConfig) {
  pfSrc1_ = iConfig.getParameter<edm::InputTag>("pfsrc1");
  pfSrc2_ = iConfig.getParameter<edm::InputTag>("pfsrc2");
  trSrc1_ = iConfig.getParameter<edm::InputTag>("trsrc1");
  trSrc2_ = iConfig.getParameter<edm::InputTag>("trsrc2");
  vtxSrc_ = iConfig.getParameter<edm::InputTag>("vtxsrc");
  produces<std::vector<reco::PFCandidate> >("");
  produces<std::vector<reco::Track> >("");
}


TauGunMerger::~TauGunMerger() {
}


void TauGunMerger::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  edm::Handle<std::vector<reco::Vertex> > vtxs;
  iEvent.getByLabel(vtxSrc_, vtxs);

  edm::Handle<std::vector<reco::PFCandidate> > pfcands;

  std::auto_ptr<std::vector<reco::PFCandidate> > allp(new std::vector<reco::PFCandidate>());

  iEvent.getByLabel(pfSrc1_, pfcands);
  for (std::vector<reco::PFCandidate>::const_iterator it = pfcands->begin(); it != pfcands->end(); ++it) {
    allp->push_back(*it);
  }
  iEvent.getByLabel(pfSrc2_, pfcands);
  for (std::vector<reco::PFCandidate>::const_iterator it = pfcands->begin(); it != pfcands->end(); ++it) {
    reco::PFCandidate c = *it;
    c.setVertex(math::XYZPoint((*vtxs)[0].x(), (*vtxs)[0].y(), (*vtxs)[0].z()));
    allp->push_back(c);
  }

  iEvent.put(allp);

  edm::Handle<std::vector<reco::Track> > tracks;

  std::auto_ptr<std::vector<reco::Track> > alltr(new std::vector<reco::Track>());

  iEvent.getByLabel(trSrc1_, tracks);
  for (std::vector<reco::Track>::const_iterator it = tracks->begin(); it != tracks->end(); ++it) {
    alltr->push_back(*it);
  }
  iEvent.getByLabel(trSrc2_, tracks);
  for (std::vector<reco::Track>::const_iterator it = tracks->begin(); it != tracks->end(); ++it) {
    alltr->push_back(*it);
  }

  iEvent.put(alltr);

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(TauGunMerger);
