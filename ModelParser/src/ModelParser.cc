// -*- C++ -*-
//
// Package:    ModelParser
// Class:      ModelParser
// 
/**\class ModelParser ModelParser.cc UserCode/ModelParser/src/ModelParser.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Thu Mar 24 16:23:59 CDT 2011
// $Id: ModelParser.cc,v 1.2 2011/07/05 19:15:23 mrenna Exp $
//
//


// system include files
#include <memory>
#include <string>
#include <sstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// LHE Event
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
//#include "GeneratorInterface/LHEInterface/interface/LHEEvent.h"

//#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
//#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
//#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"




//
// class declaration
//

class ModelParser : public edm::EDFilter {
   public:
      explicit ModelParser(const edm::ParameterSet&);
      ~ModelParser();

      typedef std::vector<std::string>::const_iterator
      comments_const_iterator;

   private:
      virtual void beginJob() ;
      virtual bool filter(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
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
ModelParser::ModelParser(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed

}


ModelParser::~ModelParser()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
ModelParser::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   Handle<LHEEventProduct> product;
   iEvent.getByLabel("source", product);

   comments_const_iterator c_begin = product->comments_begin();
   comments_const_iterator c_end = product->comments_end();

   double m0, m12, tanb, A0, mu=1.0;
   double signMu;
   for( comments_const_iterator cit=c_begin; cit!=c_end; ++cit) {
      size_t found = (*cit).find("model");
      if( found != std::string::npos)   {    
//         std::cout << *cit << std::endl;  
         size_t foundLength = (*cit).size();
         found = (*cit).find("=");
         std::string smaller = (*cit).substr(found+1,foundLength);
         found = smaller.find("_");
         smaller = smaller.substr(found+1,smaller.size());
//
         std::istringstream iss(smaller);
         iss >> m0;
         iss.clear();
//
         found = smaller.find("_");
         smaller = smaller.substr(found+1,smaller.size());
         iss.str(smaller);
         iss >> m12;
         iss.clear();
//
         found = smaller.find("_");
         smaller = smaller.substr(found+1,smaller.size());
         iss.str(smaller);
         iss >> tanb;
         iss.clear();
//
         found = smaller.find("_");
         smaller = smaller.substr(found+1,smaller.size());
         iss.str(smaller);
         iss >> A0;
         iss.clear();
//
         found = smaller.find("_");
         smaller = smaller.substr(found+1,smaller.size());
         iss.str(smaller);
         iss >> signMu;
         iss.clear();
         mu *= signMu;
      }
   }
   char buffer[100];
   int n =sprintf(buffer,"mSugra model with parameters m0=%6.2f m12=%6.2f tanb=%6.2f A0=%6.2f mu=%6.2f\n",m0,m12,tanb,A0,mu);
   std::cout << buffer ;


   return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
ModelParser::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ModelParser::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(ModelParser);
