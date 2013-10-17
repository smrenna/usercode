
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


class MultiPlotter : public edm::EDAnalyzer {

  public:

    explicit MultiPlotter(const edm::ParameterSet & iConfig);
    ~MultiPlotter();

  private:

    virtual void analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup);

    edm::Service<TFileService> fs;
    edm::InputTag mhtSource_;
    edm::InputTag htSource_;
    edm::InputTag jetSource_;
    edm::InputTag trackSource_;
    edm::InputTag vertexSource_;
    edm::InputTag ebrhSource_;
    edm::InputTag eerhSource_;
    double dzTrVtxMax_, dxyTrVtxMax_, minSumPtOverHT_;
    unsigned int maxNrRecHits_;
    TH1F * h_mht_all, * h_mht_trfail, * h_mht_beamhalo, * h_mht_eenoise, * h_mht_deadcell, * h_mht_badmuon, * h_mht_vertex;
    TH1F * h_ht_all,  * h_ht_trfail,  * h_ht_beamhalo,  * h_ht_eenoise,  * h_ht_deadcell,  * h_ht_badmuon,  * h_ht_vertex;
    TH1F * h_sumptht, * h_sumptcaloht, * h_ntracks;
    TH1F * h_neerh, * h_eeerh;
    TH2F * h_neeebrh, * h_neeerh;
    TH2F * h_maxvssumerh, * h_maxvssumhrh;
    TH1F * h_jetn90, * h_jetnconstit;

};


MultiPlotter::MultiPlotter(const edm::ParameterSet& iConfig) {
  mhtSource_      = iConfig.getParameter<edm::InputTag>("MHTSource");
  htSource_       = iConfig.getParameter<edm::InputTag>("HTSource");
  jetSource_      = iConfig.getParameter<edm::InputTag>("JetSource");
  trackSource_    = iConfig.getParameter<edm::InputTag>("TrackSource");
  vertexSource_   = iConfig.getParameter<edm::InputTag>("VertexSource");
  eerhSource_     = iConfig.getParameter<edm::InputTag>("EERecHitSource");
  ebrhSource_     = iConfig.getParameter<edm::InputTag>("EBRecHitSource");
  dzTrVtxMax_     = iConfig.getParameter<double>("DzTrVtxMax");
  dxyTrVtxMax_    = iConfig.getParameter<double>("DxyTrVtxMax");
  minSumPtOverHT_ = iConfig.getParameter<double>("MinSumPtOverHT");
  maxNrRecHits_   = iConfig.getParameter<unsigned int>("MaxNrRecHits");
  std::string mhtHistoName     = iConfig.getParameter<std::string>("MHTHistoName");
  std::string htHistoName      = iConfig.getParameter<std::string>("HTHistoName");
  std::string sumptHistoName   = iConfig.getParameter<std::string>("SumPtHistoName");
  std::string sumpthtHistoName = iConfig.getParameter<std::string>("SumPtHTHistoName");
  h_mht_all        = fs->make<TH1F>(TString(mhtHistoName.c_str())+"_all",        "MHT", 200, 0, 1500);
  h_mht_trfail     = fs->make<TH1F>(TString(mhtHistoName.c_str())+"_trfail",     "MHT", 200, 0, 1500);
  h_mht_beamhalo   = fs->make<TH1F>(TString(mhtHistoName.c_str())+"_beamhalo",   "MHT", 200, 0, 1500);
  h_mht_eenoise    = fs->make<TH1F>(TString(mhtHistoName.c_str())+"_eenoise",    "MHT", 200, 0, 1500);
  h_mht_deadcell   = fs->make<TH1F>(TString(mhtHistoName.c_str())+"_deadcell",   "MHT", 200, 0, 1500);
  h_mht_badmuon    = fs->make<TH1F>(TString(mhtHistoName.c_str())+"_badmuon",    "MHT", 200, 0, 1500);
  h_mht_vertex     = fs->make<TH1F>(TString(mhtHistoName.c_str())+"_vertex",     "MHT", 200, 0, 1500);
  h_ht_all         = fs->make<TH1F>(TString(htHistoName.c_str())+"_all",         "HT",  200, 0, 4000);
  h_ht_trfail      = fs->make<TH1F>(TString(htHistoName.c_str())+"_trfail",      "HT",  200, 0, 4000);
  h_ht_beamhalo    = fs->make<TH1F>(TString(htHistoName.c_str())+"_beamhalo",    "HT",  200, 0, 4000);
  h_ht_eenoise     = fs->make<TH1F>(TString(htHistoName.c_str())+"_eenoise",     "HT",  200, 0, 4000);
  h_ht_deadcell    = fs->make<TH1F>(TString(htHistoName.c_str())+"_deadcell",    "HT",  200, 0, 4000);
  h_ht_badmuon     = fs->make<TH1F>(TString(htHistoName.c_str())+"_badmuon",     "HT",  200, 0, 4000);
  h_ht_vertex      = fs->make<TH1F>(TString(htHistoName.c_str())+"_vertex",      "HT",  200, 0, 4000);
  h_sumptht        = fs->make<TH1F>(sumpthtHistoName.c_str(), "Sum pT / HT", 200, 0, 2);
  h_neerh          = fs->make<TH1F>("nr_eerh", "Number of EE rechits", 500, 0, 5000);
  h_eeerh          = fs->make<TH1F>("energy_eerh", "Energy of EE rechits", 500, 0, 5000);
  h_neeebrh        = fs->make<TH2F>("nreerh_nrebrh", "Nr. of EE vs. EB rechits", 500, 0, 5000, 500, 0, 5000);
  h_neeerh         = fs->make<TH2F>("nr_energy_eerh", "Number vs. energy of EE rechits", 500, 0, 5000, 500, 0, 5000);
  h_maxvssumerh    = fs->make<TH2F>("max_vs_sum_erh", "Max over sum of ECAL rechits", 200, 0, 1.2, 200, 0, 500);
  h_maxvssumhrh    = fs->make<TH2F>("max_vs_sum_hrh", "Max over sum of HCAL rechits", 200, 0, 1.2, 200, 0, 500);
  h_jetn90         = fs->make<TH1F>("jetn90", "N90 for central 50GeV jets", 50, 0, 50);
  h_jetnconstit    = fs->make<TH1F>("jetnconstit", "Nr of constit. for central 50GeV jets", 50, 0, 50);
}


MultiPlotter::~MultiPlotter() {
}


void MultiPlotter::analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup) {

  edm::Handle<edm::View<reco::MET> > mht;
  iEvent.getByLabel(mhtSource_, mht);
  edm::Handle<edm::View<reco::MET> > ht;
  iEvent.getByLabel(htSource_, ht);
  edm::Handle<edm::View<reco::Jet> > jets;
  iEvent.getByLabel(jetSource_, jets);
  edm::Handle<std::vector<reco::Track> > tracks;
  iEvent.getByLabel(trackSource_, tracks);
  edm::Handle<std::vector<reco::Vertex> > vtxs;
  iEvent.getByLabel(vertexSource_, vtxs);
  const reco::Vertex * vtx = (vtxs->size()==0 ? 0 : &((*vtxs)[0]));
  edm::Handle<reco::BeamHaloSummary> beamHaloSummary;
  iEvent.getByLabel("BeamHaloSummary" , beamHaloSummary);
  edm::Handle<EcalRecHitCollection> eerhs;
  iEvent.getByLabel(eerhSource_, eerhs);
  edm::Handle<EcalRecHitCollection> ebrhs;
  iEvent.getByLabel(ebrhSource_, ebrhs);

  float sumtrpt = 0;
  if (vtx) {
    for (std::vector<reco::Track>::const_iterator tr = tracks->begin(); tr != tracks->end(); ++tr) {
      if (fabs(tr->dz(vtx->position())) > dzTrVtxMax_) continue;
      if (fabs(tr->dxy(vtx->position())) > dxyTrVtxMax_) continue;
      sumtrpt += tr->pt();
    }
  }
  float sumjpt = 0;
  for (edm::View<reco::Jet>::const_iterator j = jets->begin(); j != jets->end(); ++j) {
    sumjpt += j->pt();
  }

  float rhsume = 0;
  for (unsigned int i = 0; i < eerhs->size(); ++i) {
    rhsume += (*eerhs)[i].energy();
  }

  // fill histograms
  h_sumptht->Fill(sumtrpt/sumjpt);
  h_neerh->Fill(eerhs->size());
  h_eeerh->Fill(rhsume);
  h_neeebrh->Fill(eerhs->size(), ebrhs->size());
  h_neeerh->Fill(eerhs->size(), rhsume);

  std::vector<float> rhe;
  for (EcalRecHitCollection::const_iterator i = eerhs->begin(); i != eerhs->end(); ++i) if (i->energy()>0 && i->checkFlag(0)) rhe.push_back( i->energy() );
  for (EcalRecHitCollection::const_iterator i = ebrhs->begin(); i != ebrhs->end(); ++i) if (i->energy()>0 && i->checkFlag(0)) rhe.push_back( i->energy() );
  std::sort(rhe.begin(), rhe.end());
  h_maxvssumerh->Fill(*(rhe.end()-2) / *(rhe.end()-1), *(rhe.end()-1));

  for (edm::View<reco::Jet>::const_iterator j = jets->begin(); j != jets->end(); ++j) {
    if (j->pt() > 50 && fabs(j->eta()) < 2.5) {
//      h_jetn90->Fill(j->n90());
      h_jetnconstit->Fill(j->numberOfDaughters());
    }
  }

  // fill for all events
  h_mht_all->Fill((*mht)[0].pt());
  h_ht_all->Fill((*ht)[0].sumEt());
  // fill for specific failures
  if (sumtrpt/sumjpt < minSumPtOverHT_) {
    h_mht_trfail->Fill((*mht)[0].pt());
    h_ht_trfail->Fill((*ht)[0].sumEt());
  }
  if (beamHaloSummary->CSCTightHaloId()) {
    h_mht_beamhalo->Fill((*mht)[0].pt());
    h_ht_beamhalo->Fill((*ht)[0].sumEt());
  }
  if (eerhs->size() > maxNrRecHits_) {
    h_mht_eenoise->Fill((*mht)[0].pt());
    h_ht_eenoise->Fill((*ht)[0].sumEt());
  }
  if (!vtx) {
    h_mht_vertex->Fill((*mht)[0].pt());
    h_ht_vertex->Fill((*ht)[0].sumEt());
  }

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(MultiPlotter);
