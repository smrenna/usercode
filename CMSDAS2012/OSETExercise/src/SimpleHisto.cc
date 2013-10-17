// -*- C++ -*-
//
// Package:    SimpleHisto
// Class:      SimpleHisto
// 
/**\class SimpleHisto SimpleHisto.cc UserCode/SimpleHisto/src/SimpleHisto.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Sat Jan 22 16:51:55 CST 2011
// $Id: SimpleHisto.cc,v 1.1.1.1 2012/01/10 17:57:48 mrenna Exp $
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

class SimpleHisto : public edm::EDAnalyzer {
   public:
      explicit SimpleHisto(const edm::ParameterSet&);
      ~SimpleHisto();


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------
      edm::InputTag src_;
      TH1D * histo; 
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
SimpleHisto::SimpleHisto(const edm::ParameterSet& iConfig) :
   src_( iConfig.getParameter<edm::InputTag>( "src" ) )

{
   //now do what ever initialization is needed
  edm::Service<TFileService> fs;
  histo = fs->make<TH1D>("mass" , "Mass" , 100 ,100., 200. );

}


SimpleHisto::~SimpleHisto()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
SimpleHisto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
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

//   TLorentzVector vpTop = TLorentzVector(pTop->px(),pTop->py(),pTop->pz(),pTop->energy());
//      histo->Fill( charge );

}


// ------------ method called once each job just before starting event loop  ------------
void 
SimpleHisto::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
SimpleHisto::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(SimpleHisto);
