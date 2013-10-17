// -*- C++ -*-
//
// Package:    LHEHTCut
// Class:      LHEHTCut
// 
/**\class LHEHTCut LHEHTCut.cc UserCode/LHEHTCut/src/LHEHTCut.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Mon Sep 19 16:53:56 CDT 2011
// $Id: LHEHTCut.cc,v 1.1.1.1 2011/09/20 13:38:15 mrenna Exp $
//
//

#include <string>
#include <sstream>


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// LHE Event
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "GeneratorInterface/LHEInterface/interface/LHEEvent.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
//#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
//#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"




//
// class declaration
//

class LHEHTCut : public edm::EDFilter {
   public:
      explicit LHEHTCut(const edm::ParameterSet&);
      ~LHEHTCut();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual bool beginRun(edm::Run&, edm::EventSetup const&);
      virtual bool endRun(edm::Run&, edm::EventSetup const&);
      virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      double htEventCut_;

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
LHEHTCut::LHEHTCut(const edm::ParameterSet& iConfig) :
   htEventCut_(iConfig.getParameter<double>("LHEHTCut"))
{
   //now do what ever initialization is needed
}


LHEHTCut::~LHEHTCut()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
LHEHTCut::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   Handle<LHEEventProduct> product;
   iEvent.getByLabel("source", product);

   const lhef::HEPEUP hepeup_ = product->hepeup();
   const std::vector<lhef::HEPEUP::FiveVector> pup_ = hepeup_.PUP;

   double htEvent = 0.0;
   size_t iMax = hepeup_.NUP;
   for(size_t i = 2; i < iMax; ++i) {
      if( hepeup_.ISTUP[i] != 1 ) continue;
      int idabs = abs( hepeup_.IDUP[i] );
      if( idabs != 21 && (idabs<1 || idabs>6) ) continue;
      double ptPart = sqrt( pow(hepeup_.PUP[i][0],2) + pow(hepeup_.PUP[i][1],2) );
//      std::cout << ptPart << std::endl;
      htEvent += ptPart;
   }

//   std::cout << htEvent << " " << htEventCut_ << std::endl;

   if( htEvent < htEventCut_ ) return false;

   return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
LHEHTCut::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
LHEHTCut::endJob() {
}

// ------------ method called when starting to processes a run  ------------
bool 
LHEHTCut::beginRun(edm::Run&, edm::EventSetup const&)
{ 
  return true;
}

// ------------ method called when ending the processing of a run  ------------
bool 
LHEHTCut::endRun(edm::Run&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool 
LHEHTCut::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool 
LHEHTCut::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
  return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
LHEHTCut::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(LHEHTCut);
