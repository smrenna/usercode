// -*- C++ -*-
//
// Package:    MassDiff
// Class:      MassDiff
// 
/**\class MassDiff MassDiff.cc UserCode/MassDiff/src/MassDiff.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Sat Jan 22 16:51:55 CST 2011
// $Id: MassDiff.cc,v 1.1.1.1 2012/01/10 17:57:48 mrenna Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Common/interface/Ref.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/Vector3D.h"

#include "TLorentzVector.h"
#include "TVector3.h"
#include "TH1D.h"
//
// class declaration
//

class MassDiff : public edm::EDAnalyzer {
   public:
      explicit MassDiff(const edm::ParameterSet&);
      ~MassDiff();


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------
      edm::InputTag src_;
      TH1D * histo; 
      TH1D * h_massdiff;
      TH1D* h_p_cosTheta_;
      TH1D* h_p_cosThetap_;
      TH1D* h_m_cosTheta_;
      TH1D* h_m_cosThetap_;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
MassDiff::MassDiff(const edm::ParameterSet& iConfig) :
   src_( iConfig.getParameter<edm::InputTag>( "src" ) )

{
   //now do what ever initialization is needed
  edm::Service<TFileService> fs;
  histo = fs->make<TH1D>("mass" , "Mass" , 100 ,100., 200. );
  h_massdiff = fs->make<TH1D>("massdiff" , "Mass Difference" , 100 ,-0.1, 0.1 );

   h_p_cosTheta_ = fs->make<TH1D>( "h_p_cosTheta", "Cos[Theta*]", 40, -1.0, 1.0 );
   h_p_cosThetap_ = fs->make<TH1D>( "h_p_cosThetap", "Cos[Theta*] corrected", 40, -1.0, 1.0 );
   h_m_cosTheta_ = fs->make<TH1D>( "h_m_cosTheta", "Cos[Theta*]", 40, -1.0, 1.0 );
   h_m_cosThetap_ = fs->make<TH1D>( "h_m_cosThetap", "Cos[Theta*] corrected", 40, -1.0, 1.0 );

}


MassDiff::~MassDiff()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
MassDiff::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace reco;

   Handle<reco::CandidateView> particles;
   iEvent.getByLabel( src_, particles );

   CandidateView::const_iterator pBoson = particles->begin(); 
   CandidateView::const_iterator mBoson = particles->begin(); 

   int iMatch=0;
   for( CandidateView::const_iterator p = particles->begin(); 
        p != particles->end(); ++ p) {
      int idabs = abs( p->pdgId() );

      if( p->status()!= 3 ) continue;
      if( p->pdgId() == 6 ) histo->Fill( p->mass() );
   }


   iMatch=0;
   for( CandidateView::const_iterator p = particles->begin(); 
        p != particles->end(); ++ p) {
      int idabs = abs( p->pdgId() );

      if( p->status()!= 3 ) continue;
      if( idabs!=37 && idabs!=24) continue;
      if( p->pdgId() > 0 ) {
         pBoson = p;
         iMatch++;
      } else {
         mBoson = p;
         iMatch++;
      }
      if( iMatch==2 ) break;
   }


   CandidateView::const_iterator pMu = particles->begin();
   CandidateView::const_iterator pNu = particles->begin();
   CandidateView::const_iterator mMu = particles->begin();
   CandidateView::const_iterator mNu = particles->begin();

   CandidateView::const_iterator pTop = particles->begin();
   CandidateView::const_iterator pBot = particles->begin();
   CandidateView::const_iterator mTop = particles->begin();
   CandidateView::const_iterator mBot = particles->begin();

   iMatch=0;
   for( CandidateView::const_iterator p = particles->begin();
        p != particles->end(); ++ p) {
//      int idabs = abs( p->pdgId() );

      if( p->status()!= 3 ) continue;

      switch( p->pdgId() ) {

         case -6:
            mTop = p;
            iMatch++;
            break;

         case -5:
            mBot = p;
            iMatch++;
            break;

         case 13:
            mMu = p;
            iMatch++;
            break;
         case -14:
            mNu = p;
            iMatch++;
            break;

         case 6:
            pTop = p;
            iMatch++;
            break;

         case 5:
            pBot = p;
            iMatch++;
            break;

         case -13:
            pMu = p;
            iMatch++;
            break;
         case 14:
            pNu = p;
            iMatch++;
            break;



         default:
            break;
      }
      if( iMatch==8 ) break;
   }

   TLorentzVector vpBoson = TLorentzVector(pBoson->px(),pBoson->py(),pBoson->pz(),pBoson->energy());
   TLorentzVector vmBoson = TLorentzVector(mBoson->px(),mBoson->py(),mBoson->pz(),mBoson->energy());

   TLorentzVector vpTop = TLorentzVector(pTop->px(),pTop->py(),pTop->pz(),pTop->energy());
   TLorentzVector vpBot = TLorentzVector(pBot->px(),pBot->py(),pBot->pz(),pBot->energy());
   TLorentzVector vpMu = TLorentzVector(pMu->px(),pMu->py(),pMu->pz(),pMu->energy());
   TLorentzVector vpNu = TLorentzVector(pNu->px(),pNu->py(),pNu->pz(),pNu->energy());

   TLorentzVector vpTopCorr = vpBot + vpMu + vpNu;
 
   double massdiff = 1.0 - vpTopCorr.M()/vpTop.M();

   h_massdiff->Fill(massdiff);

 
   TLorentzVector vpBotLab = vpBot;   

   TLorentzVector vmTop = TLorentzVector(mTop->px(),mTop->py(),mTop->pz(),mTop->energy());
   TLorentzVector vmBot = TLorentzVector(mBot->px(),mBot->py(),mBot->pz(),mBot->energy());
   TLorentzVector vmBotLab = vmBot;
   TLorentzVector vmMu = TLorentzVector(mMu->px(),mMu->py(),mMu->pz(),mMu->energy());
   TLorentzVector vmNu = TLorentzVector(mNu->px(),mNu->py(),mNu->pz(),mNu->energy());

   const Candidate &pIn1= *(pTop->mother(0));
   const Candidate &pIn2= *(pTop->mother(1));


   TLorentzVector vIn1 = TLorentzVector(pIn1.px(),pIn1.py(),pIn1.pz(),pIn1.energy());
   TLorentzVector vIn2 = TLorentzVector(pIn2.px(),pIn2.py(),pIn2.pz(),pIn2.energy());

   int iType = ( pIn1.pdgId() == 21 ) ? 1 : 0 ;


   TLorentzVector vpBosonX = vpMu + vpNu;
   TLorentzVector vmBosonX = vmMu + vmNu;

   TVector3 vpbX = -vpBosonX.BoostVector();   
   TVector3 vmbX = -vmBosonX.BoostVector();      
   vpMu.Boost(vpbX);
   vpNu.Boost(vpbX);
   vmMu.Boost(vmbX);
   vmNu.Boost(vmbX);
   TVector3 vpbY = vpBoson.BoostVector();   
   TVector3 vmbY = vmBoson.BoostVector();      
   vpMu.Boost(vpbY);
   vpNu.Boost(vpbY);
   vmMu.Boost(vmbY);
   vmNu.Boost(vmbY);


   TLorentzVector vTmp;
   TLorentzVector vpTopLab = vpTop;
   TLorentzVector vmTopLab = vmTop;
   TLorentzVector vpMuLab = vpMu;
   TLorentzVector vmMuLab = vmMu;
   TLorentzVector vpNuLab = vpNu;
   TLorentzVector vmNuLab = vmNu;


   TVector3 vpb = -vpBoson.BoostVector();   
   TVector3 vmb = -vmBoson.BoostVector();   


   vpTop.Boost(vpb);
   vpBot.Boost(vpb);
   vpMu.Boost(vpb);
   vpNu.Boost(vpb);

   vmTop.Boost(vmb);
   vmBot.Boost(vmb);
   vmMu.Boost(vmb);
   vmNu.Boost(vmb);

   double pAngle = vpMu.Angle(-vpTop.Vect());
   double mAngle = vmMu.Angle(-vmTop.Vect());

   h_p_cosTheta_->Fill(cos(pAngle));
   h_m_cosTheta_->Fill(cos(mAngle));


/*
   double newWeight_p = topDecayWeight(vpTop, vpBot, vpNu, vpMu );
   double newWeight_m = topDecayWeight(vmTop, vmBot, vmNu, vmMu );
   double newWeight = newWeight_p * newWeight_m;
*/



}

// ------------ method called once each job just after ending the event loop  ------------
void 
MassDiff::beginJob() {
}
void 
MassDiff::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(MassDiff);
