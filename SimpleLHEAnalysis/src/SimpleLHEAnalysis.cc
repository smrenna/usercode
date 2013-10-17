// -*- C++ -*-
//
// Package:    SimpleLHEAnalysis
// Class:      SimpleLHEAnalysis
// 
/**\class SimpleLHEAnalysis SimpleLHEAnalysis.cc UserCode/SimpleLHEAnalysis/src/SimpleLHEAnalysis.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Tue Jan 24 10:55:59 CST 2012
// $Id: SimpleLHEAnalysis.cc,v 1.1.1.1 2013/02/20 08:20:55 mrenna Exp $
//
//


// system include files
#include <memory>
#include <string>
#include <sstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


// LHE Event
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "TH1F.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"


#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

// class declaration
//

class SimpleLHEAnalysis : public edm::EDAnalyzer {
   public:
      explicit SimpleLHEAnalysis(const edm::ParameterSet&);
      ~SimpleLHEAnalysis();

      typedef std::vector<std::string>::const_iterator
      comments_const_iterator;

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);


      // ----------member data ---------------------------
      std::vector<std::string> modelList;
      TH1F *h_mmo, *h_ptmo, *h_etamo, *h_mda, *h_ptda, *h_etada, *h_mdcy, *h_ptdcy, *h_etadcy;
      edm::Service<TFileService> fs;
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
SimpleLHEAnalysis::SimpleLHEAnalysis(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed

}


SimpleLHEAnalysis::~SimpleLHEAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
SimpleLHEAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   Handle<reco::GenParticleCollection> particles;
   iEvent.getByLabel("genParticles",particles);


   std::vector<int> mothers;
   std::vector<int> daughters;
   std::vector<int> decays;

   mothers.push_back(6);
   mothers.push_back(7);
   daughters.push_back(8);
   daughters.push_back(11);
   decays.push_back(9);
   decays.push_back(10);
   decays.push_back(12);
   decays.push_back(13);


   Handle<LHEEventProduct> product;
   iEvent.getByLabel("source", product);

   comments_const_iterator c_begin = product->comments_begin();
   comments_const_iterator c_end = product->comments_end();

   std::string modelString;

   for( comments_const_iterator cit=c_begin; cit!=c_end; ++cit) {
      size_t found = (*cit).find("model");
      if( found != std::string::npos)   {    
//         std::cout << *cit << std::endl;  
//         size_t foundLength = (*cit).size()-9;
//         std::cout << "foundLength " << foundLength << " " << (*cit).size() << std::endl;
         char ch = ' ';
         size_t foundLength = (*cit).find(ch,found+6);
         modelString = (*cit).substr(found+6,foundLength-(found+6));
//         std::cout << found << " " << foundLength << std::endl;
//         std::cout << modelString << std::endl;
         break;
      }
   }
/*   char buffer[100];
   int n =sprintf(buffer,"model string %s\n",modelString.c_str());
   std::cout << buffer ; */

   if(std::find(modelList.begin(),modelList.end(),modelString) == modelList.end() ) {
      std::cout << "book new histogram " << modelString << std::endl;
      modelList.push_back(modelString);
      size_t foundLength = modelString.size();
      size_t found = modelString.find("_");      
      std::string smaller = modelString.substr(found+1,foundLength);
      found = smaller.find("_");
      std::istringstream iss(smaller.substr(0,found));
      float mmo;
      iss >> mmo;
//      std::cout << mmo << std::endl;
      foundLength = smaller.size();
//      std::cout << found << " " << foundLength << std::endl;
      float mda;
//      std::cout << " the string = " << smaller.substr(found+1,foundLength) << std::endl;
      iss.clear();
      iss.str(smaller.substr(found+1,foundLength));
//      std::cout << iss << std::endl;
//      std::cout << found << " " << foundLength << std::endl;
      iss >> mda;
//     std::cout << mda << std::endl;
      if( mda<0.0 ) mda=0.0;
      
      TFileDirectory subDir = fs->mkdir(modelString.c_str());
      h_mmo = subDir.make<TH1F>(("h_mmo"),("h_mmo"),100,0.75*mmo,1.25*mmo);
      h_ptmo = subDir.make<TH1F>(("h_ptmo"),("h_ptmo"),100,0.0,1.5*mmo);
      h_etamo = subDir.make<TH1F>("h_rapmo","h_rapmo",100,-5.0,5.0);
      h_mda = subDir.make<TH1F>(("h_mda"),("h_mda"),100,0.75*mda,1.25*(mmo-mda));
      h_ptda = subDir.make<TH1F>(("h_ptda"),("h_ptda"),100,0.0,1.5*mmo);
      h_etada = subDir.make<TH1F>("h_rapda","h_rapda",100,-5.0,5.0);
      h_mdcy = subDir.make<TH1F>(("h_mdcy"),("h_mdcy"),100,0.75*mda,1.25*(mmo-mda));
      h_ptdcy = subDir.make<TH1F>(("h_ptdcy"),("h_ptdcy"),100,0.0,1.5*mmo);
      h_etadcy = subDir.make<TH1F>("h_rapdcy","h_rapdcy",100,-5.0,5.0);
   }

   for( std::vector<int>::const_iterator cit = mothers.begin(); cit != mothers.end(); ++cit) {
      size_t id = (*cit);
      const reco::GenParticle *p0 = &(*particles)[id];
      h_mmo -> Fill(p0->mass());      
      h_ptmo -> Fill(p0->pt());
      h_etamo -> Fill(p0->rapidity());
   }

   for( std::vector<int>::const_iterator cit = daughters.begin(); cit != daughters.end(); ++cit) {
      int id = (*cit);
      const reco::GenParticle *p0 = &(*particles)[id];
      h_mda -> Fill(p0->mass());      
      h_ptda -> Fill(p0->pt());
      h_etada -> Fill(p0->rapidity());
   }
   for( std::vector<int>::const_iterator cit = decays.begin(); cit != decays.end(); ++cit) {
      int id = (*cit);
      const reco::GenParticle *p0 = &(*particles)[id];
      h_mdcy -> Fill(p0->mass());      
      h_ptdcy -> Fill(p0->pt());
      h_etadcy -> Fill(p0->rapidity());
   }

}


// ------------ method called once each job just before starting event loop  ------------
void 
SimpleLHEAnalysis::beginJob()
{

}

// ------------ method called once each job just after ending the event loop  ------------
void 
SimpleLHEAnalysis::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
SimpleLHEAnalysis::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
SimpleLHEAnalysis::endRun(edm::Run const&, edm::EventSetup const&)
{

   comments_const_iterator c_begin = modelList.begin();
   comments_const_iterator c_end = modelList.end();
   for(std::vector<std::string>::const_iterator cit=c_begin; cit!=c_end; ++cit) {
      std::cout << "model " << (*cit) << std::endl;
   }


}

// ------------ method called when starting to processes a luminosity block  ------------
void 
SimpleLHEAnalysis::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
SimpleLHEAnalysis::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
SimpleLHEAnalysis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(SimpleLHEAnalysis);
