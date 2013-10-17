
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PileUpPFCandidate.h"
#include "RecoVertex/PrimaryVertexProducer/interface/VertexHigherPtSquared.h"
#include "TH1F.h"
#include "TH2F.h"


class VertexPlotter : public edm::EDAnalyzer {

  public:

    explicit VertexPlotter(const edm::ParameterSet & iConfig);
    ~VertexPlotter();

  private:

    virtual void analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup);

    edm::Service<TFileService> fs;
    edm::InputTag vtxSource_, trSource_, metSource_, jetSource_, pfCands_, puCands_, rhoSource_;
    TH1F * h_trxy  [5], * h_trz  [5], * h_trxyzoom[5], * h_trzzoom[5];
    TH1F * h_vxy   [5], * h_vz   [5], * h_vxyzoom [5], * h_vzzoom [5];
    TH1F * h_dxy   [5], * h_dz   [5], * h_dxyzoom [5], * h_dzzoom [5];
    TH1F * h_ntr   [5], * h_sumpt[5], * h_nchi2[5];
    TH1F * h_met[5], * h_ht[5], * h_njets[5], * h_chf[5];
    TH1F * h_vtxminpt[5], * h_vtxavgpt[5], * h_vtxmaxpt[5], * h_vtxdpt[5], * h_vtxdn[5];
    TH1F * h_chsdpt[5], * h_chsdn[5], * h_rho[5];

};


VertexPlotter::VertexPlotter(const edm::ParameterSet& iConfig) {
  vtxSource_ = iConfig.getParameter<edm::InputTag>("VertexSource");
  trSource_  = iConfig.getParameter<edm::InputTag>("TrackSource");
  metSource_ = iConfig.getParameter<edm::InputTag>("METSource");
  jetSource_ = iConfig.getParameter<edm::InputTag>("JetSource");
  pfCands_   = iConfig.getParameter<edm::InputTag>("PFCands");
  puCands_   = iConfig.getParameter<edm::InputTag>("PUCands");
  rhoSource_ = iConfig.getParameter<edm::InputTag>("RhoSource");
  TString strvtx[5] = { "all", "best", "good", "badxy", "badz" };
  for (int j = 0; j < 5; ++j) {
 	TString histoname = "h_";
    histoname += strvtx[j];
    h_trxy    [j] = fs->make<TH1F>(histoname+"_trxy"    , "", 100,    0,    1);
    h_trz     [j] = fs->make<TH1F>(histoname+"_trz"     , "", 100, -100,  100);
    h_trxyzoom[j] = fs->make<TH1F>(histoname+"_trxyzoom", "", 200,    0,  0.2);
    h_trzzoom [j] = fs->make<TH1F>(histoname+"_trzzoom" , "", 200,  -10,   10);
    h_vxy     [j] = fs->make<TH1F>(histoname+"_vxy"     , "", 100,    0,    1);
    h_vz      [j] = fs->make<TH1F>(histoname+"_vz"      , "", 100, -100,  100);
    h_vxyzoom [j] = fs->make<TH1F>(histoname+"_vxyzoom" , "", 200,    0,  0.2);
    h_vzzoom  [j] = fs->make<TH1F>(histoname+"_vzzoom"  , "", 200,  -10,   10);
    h_ntr     [j] = fs->make<TH1F>(histoname+"_ntr"     , "", 200,    0,  200);
    h_sumpt   [j] = fs->make<TH1F>(histoname+"_sumpt"   , "", 100,    0,  200);
    h_nchi2   [j] = fs->make<TH1F>(histoname+"_nchi2"   , "", 100,    0,    5);
    h_dxy     [j] = fs->make<TH1F>(histoname+"_dxy"     , "", 100,    0,    1);
    h_dz      [j] = fs->make<TH1F>(histoname+"_dz"      , "", 100,  -50,   50);
    h_dxyzoom [j] = fs->make<TH1F>(histoname+"_dxyzoom" , "", 200,    0,  0.2);
    h_dzzoom  [j] = fs->make<TH1F>(histoname+"_dzzoom"  , "", 200,  -10,   10);
    h_met     [j] = fs->make<TH1F>(histoname+"_met"     , "", 200,    0,  400);
    h_ht      [j] = fs->make<TH1F>(histoname+"_ht"      , "", 200,    0, 2000);
    h_njets   [j] = fs->make<TH1F>(histoname+"_njets"   , "",  20,    0,   20);
    h_chf     [j] = fs->make<TH1F>(histoname+"_chf"     , "", 200,    0,    1);
    h_vtxdpt  [j] = fs->make<TH1F>(histoname+"_vtxdpt"  , "", 200,    0,    1);
    h_vtxdn   [j] = fs->make<TH1F>(histoname+"_vtxdn"   , "", 200,    0,    2);
    h_vtxminpt[j] = fs->make<TH1F>(histoname+"_vtxminpt", "", 200,    0,   20);
    h_vtxavgpt[j] = fs->make<TH1F>(histoname+"_vtxavgpt", "", 200,    0,   20);
    h_vtxmaxpt[j] = fs->make<TH1F>(histoname+"_vtxmaxpt", "", 200,    0,  200);
    h_chsdpt  [j] = fs->make<TH1F>(histoname+"_chsdpt"  , "", 200,    0,    1);
    h_chsdn   [j] = fs->make<TH1F>(histoname+"_chsdn"   , "", 200,    0,    1);
    h_rho     [j] = fs->make<TH1F>(histoname+"_rho"     , "", 200,    0,   20);
  }
}


VertexPlotter::~VertexPlotter() {
}


void VertexPlotter::analyze(const edm::Event & iEvent, const edm::EventSetup & iSetup) {

  edm::Handle<std::vector<reco::Vertex> > vertices;
  iEvent.getByLabel(vtxSource_, vertices);
  edm::Handle<std::vector<reco::Track> > tracks;
  iEvent.getByLabel(trSource_, tracks);
  edm::Handle<edm::View<reco::MET> > met;
  iEvent.getByLabel(metSource_, met);
  edm::Handle<std::vector<reco::PFJet> > jets;
  iEvent.getByLabel(jetSource_, jets);
  edm::Handle<std::vector<reco::PFCandidate> > pfcands;
  iEvent.getByLabel(pfCands_, pfcands);
  edm::Handle<std::vector<reco::PileUpPFCandidate> > pucands;
  iEvent.getByLabel(puCands_, pucands);
  edm::Handle<double> rho;
  iEvent.getByLabel(rhoSource_, rho);

  int njets = 0;
  float ht = 0;
  float chf = 0;
  for (std::vector<reco::PFJet>::const_iterator jet = jets->begin(); jet != jets->end(); ++jet) {
    if (jet->pt() > 30) {
      ht += jet->pt();
      ++njets;
      chf += jet->chargedHadronEnergyFraction()+jet->chargedEmEnergyFraction()+jet->chargedMuEnergyFraction();
    }
  }
  chf /= njets;

  int ncandspf = 0, ncandspu = 0;
  float ptsumpf = 0, ptsumpu = 0;
  for (std::vector<reco::PFCandidate>::const_iterator c = pfcands->begin(); c != pfcands->end(); ++c) {
    ++ncandspf;
    ptsumpf += pow(c->pt(),2);
  }
  for (std::vector<reco::PileUpPFCandidate>::const_iterator c = pucands->begin(); c != pucands->end(); ++c) {
    ++ncandspu;
    ptsumpu += pow(c->pt(),2);
  }

  /*
  float chsmin = -999, chs = 0;
  int nchs = 0;
  for (std::vector<reco::PFJet>::const_iterator jet1 = rawjets->begin(); jet1 != rawjets->end(); ++jet1) {
    for (std::vector<reco::PFJet>::const_iterator jet2 = chsjets->begin(); jet2 != chsjets->end(); ++jet2) {
      if ((jet1->pt() > 30 || jet2->pt() > 30) && jet1->getPFConstituents()[0].key() == jet2->getPFConstituents()[0].key()) {
    	++nchs;
        float chstmp = jet2->pt()/jet1->pt();
        std::cout << jet1->phi() << " " << jet2->phi() << " " << jet1->pt() << " " << jet2->pt() << " " << chstmp << std::endl;
        if (chsmin == -999 || chstmp < chsmin) chsmin = chstmp;
        chs += chstmp;
      }
    }
  }
  chs /= nchs;
  */

  // determine best vertex
  int sumptidx = -1;
  VertexHigherPtSquared pt2Calculator;
  float sumpt2 = 0, sumpt2_0 = 0, sumpt2_1 = 0;
  for (unsigned int i = 0; i < vertices->size(); ++i) {
    float sumpt2i = pt2Calculator.sumPtSquared((*vertices)[i]);
    if (sumpt2i > sumpt2) { sumpt2 = sumpt2i; sumptidx = i; }
    if (i == 0) sumpt2_0 = sumpt2i;
    if (i == 1) sumpt2_1 = sumpt2i;
  }
  if (sumptidx == -1) return;
  if (sumptidx != 0) std::cout << "OOOOOPS!!! First vertex not the best one???" << std::endl;
  float vtxdpt = (vertices->size() > 1 ? sqrt(sumpt2_1)/sqrt(sumpt2_0) : 0);
  float vtxdn  = (vertices->size() > 1 ? 1.*(*vertices)[1].tracksSize()/(*vertices)[0].tracksSize() : 0);
  float vtxminpt = 99999, vtxavgpt = 0, vtxmaxpt = 0;
  for (std::vector<edm::RefToBase<reco::Track> >::const_iterator tr = (*vertices)[0].tracks_begin(); tr != (*vertices)[0].tracks_end(); ++tr) {
    if ((*tr)->pt() < vtxminpt) vtxminpt = (*tr)->pt();
    if ((*tr)->pt() > vtxmaxpt) vtxmaxpt = (*tr)->pt();
    vtxavgpt += (*tr)->pt();
  }
  vtxavgpt /= (*vertices)[0].tracksSize();

  if (tracks->size() == 0) return;
  const reco::Track * track = &((*tracks)[0]);


  for (unsigned int k = 0; k < 5; ++k) {
    if (k == 2 && (sqrt(pow((*vertices)[sumptidx].x()-track->vx(),2)+pow((*vertices)[sumptidx].y()-track->vy(),2)) > 0.02 ||
                   fabs((*vertices)[sumptidx].z()-track->vz()) > 1)) continue;
    if (k == 3 &&  sqrt(pow((*vertices)[sumptidx].x()-track->vx(),2)+pow((*vertices)[sumptidx].y()-track->vy(),2)) <= 0.02) continue;
    if (k == 4 &&  fabs((*vertices)[sumptidx].z()-track->vz()) <= 1) continue;
    // fill track info
    for (unsigned int i = 0; i < tracks->size(); ++i) {
      if (k > 0 && i != 0) continue;
      h_trxy    [k]->Fill(track->d0());
      h_trxyzoom[k]->Fill(track->d0());
      h_trz     [k]->Fill(track->vz());
      h_trzzoom [k]->Fill(track->vz());
    }
    // fill vertex info
    for (unsigned int i = 0; i < vertices->size(); ++i) {
      if (k > 0 && ((int) i) != sumptidx) continue;
      h_vxy    [k]->Fill(sqrt(pow((*vertices)[i].x(),2)+pow((*vertices)[i].y(),2)));
      h_vxyzoom[k]->Fill(sqrt(pow((*vertices)[i].x(),2)+pow((*vertices)[i].y(),2)));
      h_vz     [k]->Fill((*vertices)[i].z());
      h_vzzoom [k]->Fill((*vertices)[i].z());
      h_ntr    [k]->Fill((*vertices)[i].tracksSize());
      h_sumpt  [k]->Fill(sqrt(pt2Calculator.sumPtSquared((*vertices)[i])));
      h_nchi2  [k]->Fill((*vertices)[i].normalizedChi2());
      // fill vertex-track diff info
      h_dxy    [k]->Fill(sqrt(pow((*vertices)[i].x()-track->vx(),2)+pow((*vertices)[i].y()-track->vy(),2)));
      h_dxyzoom[k]->Fill(sqrt(pow((*vertices)[i].x()-track->vx(),2)+pow((*vertices)[i].y()-track->vy(),2)));
      h_dz     [k]->Fill((*vertices)[i].z()-track->vz());
      h_dzzoom [k]->Fill((*vertices)[i].z()-track->vz());
    }
    // fill event info
    h_met     [k]->Fill((*met)[0].pt());
    h_ht      [k]->Fill(ht);
    h_njets   [k]->Fill(njets);
    h_chf     [k]->Fill(chf);
    h_vtxdpt  [k]->Fill(vtxdpt);
    h_vtxdn   [k]->Fill(vtxdn);
    h_vtxminpt[k]->Fill(vtxminpt);
    h_vtxavgpt[k]->Fill(vtxavgpt);
    h_vtxmaxpt[k]->Fill(vtxmaxpt);
    h_chsdpt  [k]->Fill(sqrt(ptsumpf/(ptsumpf+ptsumpu)));
    h_chsdn   [k]->Fill(1.*ncandspf/(ncandspf+ncandspu));
    h_rho     [k]->Fill(*rho);
  }

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(VertexPlotter);
