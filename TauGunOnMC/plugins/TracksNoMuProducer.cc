
#include <memory>
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/MuonReco/interface/Muon.h"


class TracksNoMuProducer : public edm::EDProducer {

  public:

    explicit TracksNoMuProducer(const edm::ParameterSet & iConfig);
    ~TracksNoMuProducer();

    virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);

  private:

    edm::InputTag tracksLabel_;
    edm::InputTag muonsLabel_;

};


TracksNoMuProducer::TracksNoMuProducer(const edm::ParameterSet & iConfig) {
  tracksLabel_ = iConfig.getParameter<edm::InputTag>("TrackCollection");
  muonsLabel_  = iConfig.getParameter<edm::InputTag>("MuonCollection");
  produces<std::vector<reco::Track> >("TracksNoMu");
  produces<std::vector<reco::Track> >("TracksMu");
}


TracksNoMuProducer::~TracksNoMuProducer() {
}


void TracksNoMuProducer::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  // read in the objects
  edm::Handle<std::vector<reco::Track> > tracks;
  iEvent.getByLabel(tracksLabel_, tracks);
  edm::Handle<edm::View<reco::Muon> > muons;
  iEvent.getByLabel(muonsLabel_, muons);

  // produce muon-stripped collection
  std::auto_ptr<std::vector<reco::Track> > trp(new std::vector<reco::Track>());
  std::auto_ptr<std::vector<reco::Track> > mup(new std::vector<reco::Track>());
  for (std::vector<reco::Track>::const_iterator ittr = tracks->begin(); ittr != tracks->end(); ++ittr) {
    bool isMuon = false;
    for (edm::View<reco::Muon>::const_iterator itm = muons->begin(); itm != muons->end(); ++itm) {
      if (itm->innerTrack().get() == &*ittr) {
        if (itm->pt() > 10) isMuon = true;
      }
    }
    isMuon ? mup->push_back(*ittr) : trp->push_back(*ittr);
  }

  iEvent.put(trp, "TracksNoMu");
  iEvent.put(mup, "TracksMu");

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(TracksNoMuProducer);
