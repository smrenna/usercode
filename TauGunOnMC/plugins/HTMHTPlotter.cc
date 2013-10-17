
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "TH1F.h"
#include "TH2F.h"


class HTMHTPlotter : public edm::EDAnalyzer {

  public:

    explicit HTMHTPlotter(const edm::ParameterSet & iConfig);
    ~HTMHTPlotter();

  private:

    virtual void analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup);

    edm::Service<TFileService> fs;
    std::vector<edm::InputTag> mhtSource_;
    std::vector<edm::InputTag> htSource_;
    std::vector<TH1F *> h_mht;
    std::vector<TH1F *> h_ht;

};


HTMHTPlotter::HTMHTPlotter(const edm::ParameterSet& iConfig) {
  mhtSource_ = iConfig.getParameter<std::vector<edm::InputTag> >("MHTSource");
  htSource_  = iConfig.getParameter<std::vector<edm::InputTag> >("HTSource");
  std::vector<std::string> mhtHistoName = iConfig.getParameter<std::vector<std::string> >("MHTHistoName");
  std::vector<std::string> htHistoName  = iConfig.getParameter<std::vector<std::string> >("HTHistoName");
  for (unsigned int i = 0; i < mhtSource_.size() && i < mhtHistoName.size(); ++i) {
    h_mht.push_back( fs->make<TH1F>(TString(mhtHistoName[i].c_str()), "MHT (GeV)", 100, 0, 500) );
  }
  for (unsigned int i = 0; i < htSource_.size() && i < htHistoName.size(); ++i) {
    h_ht.push_back( fs->make<TH1F>(TString(htHistoName[i].c_str()), "HT (GeV)", 100, 0, 1000) );
  }
}


HTMHTPlotter::~HTMHTPlotter() {
}


void HTMHTPlotter::analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup) {

  edm::Handle<edm::View<reco::MET> > mht;
  for (unsigned int i = 0; i < h_mht.size(); ++i) {
    iEvent.getByLabel(mhtSource_[i], mht);
    if (mht.isValid() && !mht.failedToGet()) h_mht[i]->Fill((*mht)[0].pt());
  }

  edm::Handle<edm::View<reco::MET> > ht;
  for (unsigned int i = 0; i < h_ht.size(); ++i) {
    iEvent.getByLabel(htSource_[i], ht);
    if (ht.isValid() && !ht.failedToGet()) h_ht[i]->Fill((*ht)[0].sumEt());
  }

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(HTMHTPlotter);
