// -*- C++ -*-
//
// Package:    LeptonJets
// Class:      LeptonJets
// 
/**\class LeptonJets LeptonJets.cc UserCode/LeptonJets/src/LeptonJets.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Thu Apr 14 16:13:45 CDT 2011
// $Id: LeptonJets.cc,v 1.1.1.1 2011/06/23 21:07:21 mrenna Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Particle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//
// class declaration
//

class LeptonJets : public edm::EDAnalyzer {
   public:
      explicit LeptonJets(const edm::ParameterSet&);
      ~LeptonJets();


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      double allDecays;
      double electronDecays;


      // ----------member data ---------------------------
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
LeptonJets::LeptonJets(const edm::ParameterSet& iConfig) : allDecays(0), electronDecays(0)

{
   //now do what ever initialization is needed

}


LeptonJets::~LeptonJets()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
LeptonJets::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   Handle<reco::GenParticleCollection> pIn;
   try{
     iEvent.getByLabel("genParticles",pIn);
   } catch (std::exception& ex) {
     std::cout << "did not find product " << std::endl;
     return;
   }

   for( reco::GenParticleCollection::const_iterator cit=pIn->begin(); cit!=pIn->end(); ++cit ) {

         if( cit->pdgId() == 3000005 && cit->status()>2) {
//         std::cout << cit->numberOfDaughters() << std::endl;
//         std::cout << cit->daughter(0)->pdgId() << std::endl;
         int dauId = cit->daughter(1)->pdgId();
//         std::cout << " dauID = " << dauId << std::endl;
         allDecays++;
         if( dauId == 3000001 ) electronDecays++;
      }
   }



}


// ------------ method called once each job just before starting event loop  ------------
void 
LeptonJets::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
LeptonJets::endJob() {

   std::cout << " Decay Info " << electronDecays << " " << allDecays << " " << electronDecays/allDecays << std::endl;

}

//define this as a plug-in
DEFINE_FWK_MODULE(LeptonJets);
