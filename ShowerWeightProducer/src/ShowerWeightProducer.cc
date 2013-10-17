// -*- C++ -*-
//
// Package:    ShowerWeightProducer
// Class:      ShowerWeightProducer
// 
/**\class ShowerWeightProducer ShowerWeightProducer.cc UserCode/ShowerWeightProducer/src/ShowerWeightProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Wed Oct 24 17:09:34 CDT 2012
// $Id: ShowerWeightProducer.cc,v 1.1.1.1 2012/12/18 21:31:06 mrenna Exp $
//
//


// system include files
#include <memory>
#include <sstream>
#include <string>
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/Run.h"

#include "GeneratorInterface/Pythia6Interface/interface/Pythia6Declarations.h"

#include "HepMC/GenEvent.h"
#include "HepMC/PdfInfo.h"
#include "HepMC/PythiaWrapper6_4.h"
#include "HepMC/HEPEVT_Wrapper.h"

#include "GeneratorInterface/LHEInterface/interface/LHERunInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHECommonBlocks.h"
//#include "GeneratorInterface/PartonShowerVeto/interface/JetMatching.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "fastjet/JetDefinition.hh"
#include "fastjet/ClusterSequence.hh"

//
// class declaration
//

class ShowerWeightProducer : public edm::EDProducer {
   public:
      explicit ShowerWeightProducer(const edm::ParameterSet&);
      ~ShowerWeightProducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      //virtual void endRun(edm::Run&, edm::EventSetup const&);
      //virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      //virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------
      fastjet::JetDefinition fJetDefinition;
      double qCut;
      edm::ParameterSetID lastPSetId_;
      std::string parameterSource_;

};

//
// constants, enums and typedefs
//
typedef std::vector<std::string>::const_iterator comments_const_iterator;
typedef std::vector<LHERunInfoProduct::Header>::const_iterator headers_const_iterator;

int minusOne=-1;
int zero=0;
int one=1;
int two=2;

//
// static data member definitions
//
#define pyrand pyrand_ 
#define pyscat pyscat_
#define pyevol pyevol_
#define pyveto pyveto_
#define pymihk pymihk_
#define pymirm pymirm_
#define pylhef pylhef_
#define pylist pylist_
#define pyevnt pyevnt_
//#define pyinit pyinit_
#define pyptisint  pyptisint_
extern "C" {
   void pyrand();
   void pyscat();
   void pyevol(int*,double*,double*);
   void pyveto(int*);
   void pylist(int*);
//   void pyinit(char*,char*,char*,double*);
   void pymihk(); 
   void pymirm();
   void pylhef();
   void pyevnt();
   void pyptisint(int*,double*,double*,double*,int*);
}


//
// constructors and destructor
//
ShowerWeightProducer::ShowerWeightProducer(const edm::ParameterSet& iConfig) : 
   qCut(-1),
   parameterSource_(iConfig.exists("parameterSource") ? iConfig.getParameter<std::string>("parameterSource") : "HLT" )
{
   //register your products

   produces<std::vector<double> >("weight");

   //now do what ever other initialization is needed
   fJetDefinition = fastjet::JetDefinition(fastjet::kt_algorithm, 1.0 , fastjet::E_scheme);
  
}


ShowerWeightProducer::~ShowerWeightProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
ShowerWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   std::auto_ptr<std::vector<double> > weightOut(new std::vector<double>);

   using namespace edm;
   using namespace reco;

   Handle<GenParticleCollection> genPart_;
   try {
      iEvent.getByLabel("genParticles", genPart_);
   } catch (std::exception& ex) {
      std::cout << "genParticles not found " << std::endl;
      return;
   }


   Handle<LHEEventProduct> lheEvent_;
   try {
      iEvent.getByLabel("source", lheEvent_);
   } catch (std::exception& ex) {
      std::cout << "lheEvent not found " << std::endl;
      return;
   }


//Set up the Pythia parameters and initialize

   ParameterSet myPSet;
   try {
//      iEvent.getProcessParameterSet("HLT",myPSet);
      iEvent.getProcessParameterSet(parameterSource_,myPSet);
   } catch (std::exception& ex) {
      std::cout << "parameterSet not found " << std::endl;
      return;
   }
   
   if( lastPSetId_  != myPSet.id() ) {
      lastPSetId_  = myPSet.id();
      const ParameterSet& generator = myPSet.getParameter<ParameterSet>("generator");
      const ParameterSet& pythiaParams = generator.getParameter<ParameterSet>("PythiaParameters");
      std::vector<std::string> procParams = pythiaParams.getParameter<std::vector<std::string> >("processParameters");
      for(auto const& line:procParams) gen::call_pygive(line.c_str());
      std::vector<std::string> ueSettings = pythiaParams.getParameter<std::vector<std::string> >("pythiaUESettings");
      for(auto const& line:ueSettings) gen::call_pygive(line.c_str());
 //     gen::call_pygive("MSTP(143)=1");
/*      gen::call_pygive("MSTP(81)=10");
      gen::call_pygive("MSTP(61)=0");
      gen::call_pygive("MSTP(71)=0");
      gen::call_pygive("MSTP(91)=0");
      gen::call_pygive("MSTP(111)=0");*/
      gen::call_pygive("MSTP(163)=55"); 
      call_pyinit("USER"," "," ",0.0);
      gen::call_pygive("PARP(72)=");
      pyint1.vint[0]= heprup_.ebmup[0] + heprup_.ebmup[1];
      pyint1.vint[1]= pow(pyint1.vint[0],2);
   }

   GenParticleCollection::const_iterator p_begin = genPart_->begin();
   GenParticleCollection::const_iterator p_end = genPart_->end();


   std::vector<fastjet::PseudoJet> vecs1, vecs2;

   GenParticleCollection::const_iterator pisrOne = p_begin+2;
   GenParticleCollection::const_iterator pisrTwo = p_begin+3;
   GenParticleCollection::const_iterator pisrA = p_begin+4;
   GenParticleCollection::const_iterator pisrB = p_begin+5;

//Make collections of the ISR particles
   std::vector<const reco::Candidate* > cands;
   std::vector<const reco::Candidate*  >::const_iterator found = cands.begin();
   for(GenParticleCollection::const_iterator p = p_begin; p != p_end; ++p) cands.push_back(&*p);

   double pTApprox = ( (pisrA)->pt() > (pisrB)->pt() ) ? (pisrA)->pt() : (pisrB)->pt() ;

   int idx=0;
   for(GenParticleCollection::const_iterator p = p_begin; p != p_end; ++p, ++idx) {
      if( p->status() == 3 ) continue;
      int iMo1 = -1;
      found = find(cands.begin(), cands.end(), p->mother(0));
      if( found != cands.end() ) iMo1 = found - cands.begin();
//      if( p->mother(0) == &*pisrOne ) {
      if( iMo1 == 2 ) {
         fastjet::PseudoJet fastTemp = fastjet::PseudoJet(p->px(),p->py(),p->pz(),p->energy());
         fastTemp.set_user_index( idx );
         vecs1.push_back(fastTemp);         
//      } else if ( p->mother(0) == &*pisrTwo ) {
      } else if ( iMo1 == 3 ) {
         fastjet::PseudoJet fastTemp = fastjet::PseudoJet(p->px(),p->py(),p->pz(),p->energy());
         fastTemp.set_user_index( idx );
         vecs2.push_back(fastTemp);         
      }
   }
   
   double pTone = -1;
   double pTtwo = -1;

   if( vecs1.size() > 0 ) { 
     fastjet::ClusterSequence cseq1(vecs1, fJetDefinition);
     std::vector<fastjet::PseudoJet> isrJets1 = sorted_by_pt(cseq1.inclusive_jets(qCut));
     pTone = ( isrJets1.size()>0 ) ? isrJets1[0].perp() : 0.0;
   }

   if( vecs2.size() > 0 ) {
     fastjet::ClusterSequence cseq2(vecs2, fJetDefinition);
     std::vector<fastjet::PseudoJet> isrJets2 = sorted_by_pt(cseq2.inclusive_jets(qCut));
     pTtwo = ( isrJets2.size()>0 ) ? isrJets2[0].perp() : 0.0;
   }

   const lhef::HEPEUP hepeupx_ = lheEvent_->hepeup();

   const int nup_ = hepeupx_.NUP; 
   hepeup_.nup = hepeupx_.NUP; 
   const std::vector<int> idup_ = hepeupx_.IDUP;
   const std::vector<int> istup_ = hepeupx_.ISTUP;

   for(size_t i=0; i< idup_.size() ; ++i) {
      hepeup_.idup[i] = idup_[i];
      hepeup_.istup[i] = istup_[i];
      hepeup_.mothup[i][0] = hepeupx_.MOTHUP[i].first;
      hepeup_.mothup[i][1] = hepeupx_.MOTHUP[i].second;
      for(size_t j=0; j< 5; ++j) 
         hepeup_.pup[i][j] = hepeupx_.PUP[i][j];
      hepeup_.icolup[i][0] = hepeupx_.ICOLUP[i].first;
      hepeup_.icolup[i][1] = hepeupx_.ICOLUP[i].second;
   }

   hepeup_.idprup = hepeupx_.IDPRUP;
   hepeup_.xwgtup = hepeupx_.XWGTUP;
   hepeup_.scalup = hepeupx_.SCALUP;
   
   double pT2max=0;
   double qScale = hepeupx_.SCALUP;
// * sqrt( pypars.parp[63] );

   double pTshow = (pTone > pTtwo) ? pTone : pTtwo;

   double pTshow0 = pTshow;

   pTshow = pTApprox;

   double localQCut = (qCut > pTshow) ? qCut : pTshow ;

   double pT2min=pow(localQCut,2);

   double pTmin = sqrt(pT2min);

//   int iSeven=7;
//   pylist(&iSeven);
//C...Absolute max pT2 scale for evolution: phase space limit.
//   pyevnt();
//   pylhef();
//C...Check if more constrained by ISR and MI max scales:
   pyint1.vint[54]= hepeupx_.SCALUP;
   pyint1.vint[55]= pow(pyint1.vint[54],2);

   double rFac = ( pypars.parp[66] > 1.0 ) ? pypars.parp[66] : 1.0;
   double pT2max0 = std::max( rFac*pyint1.vint[55] , pyint1.vint[61] );
   double PT2MXS=   std::min( 0.25*pyint1.vint[1] , pT2max0 );
   double PT2NOW=PT2MXS;
   if( PT2NOW < pT2min ) {
      std::cout << " large scales " << sqrt(PT2NOW) << " " << pTmin << std::endl;
      PT2NOW = 1.1*pT2min;
   }
   double PT2CUT=pow(pTmin,2);
   pyint1.mint[35]=1;
   double pt2=-1;
   int ifail=0;
   double sud[2][5]={{0.0}};
   double dsud[2][5]={{0.0}};
   pyptisint(&minusOne,&PT2NOW,&PT2CUT,&pt2,&ifail);
//   std::cout << sqrt(PT2NOW) << " " << sqrt(PT2CUT) << " " << std::endl;
   for(int js=1; js<3; ++js) {
      pyint1.mint[29]=js;
      PT2NOW=PT2MXS;
      pyptisint(&zero,&PT2NOW,&PT2CUT,&pt2,&ifail);
      for(int ival=0; ival<5; ++ival) {
         sud[js-1][ival] =pyint1.vint[399-ival];
         dsud[js-1][ival]=pyint1.vint[394-ival];
      } 
   }
   double prob0[5]={0};
   double prob1[5]={0};
   for(int ival=0; ival<5; ++ival) {
      prob0[ival]=sud[0][ival]*sud[1][ival];
      prob1[ival]=sud[0][ival]*dsud[1][ival]+dsud[0][ival]*sud[1][ival];
   }

//   printf("0 -->  %6.3f  |  %7.4f  %7.4f  %7.4f  \n",pTmin,prob0[0],prob0[1],prob0[2]);
//   printf("1 -->  %6.3f  |  %7.4f  %7.4f  %7.4f  \n",pTmin,prob1[0],prob1[1],prob1[2]);

  

   double test=-1;
   if( localQCut > qCut ) {
      weightOut->push_back(prob1[1]);
      weightOut->push_back(prob1[0]);
      weightOut->push_back(prob1[2]);

      test = prob1[1]/prob1[0];
//      printf("%f %f %f \n",prob1[0],prob1[1],prob1[2]);
   } else {
      weightOut->push_back(prob0[1]);
      weightOut->push_back(prob0[0]);
      weightOut->push_back(prob0[2]);

      test = prob0[1]/prob0[0];
//      printf("%f %f %f \n",prob0[0],prob0[1],prob0[2]);

   }

   iEvent.put(weightOut,std::string("weight")); 

   if( ! ( (test < 10.0) && (test > 0.0) ) ) {
      for(int ival=0; ival<5; ++ival) {
         std::cout << "sud = " << pyint1.vint[399-ival] << std::endl;
         std::cout << "dsud= " << pyint1.vint[394-ival] << std::endl;
      } 


      int seven=7;
      pylist(&seven);
      std::cout << "pTmin " << pTmin << " " << prob0[1] << " " << prob0[0] << std::endl;
      std::cout << "pTmin " << pTmin << " " << prob1[1] << " " << prob1[0] << std::endl;
      pylhef();
      std::cout << "pTone, pTtwo = " << pTone << " " << pTtwo << std::endl;
      for(size_t i=0; i<vecs1.size(); ++i) {
         printf("%4d %9.3f %9.3f %9.3f \n",(int) i,vecs1[i].perp(),vecs1[i].eta(),vecs1[i].phi());
      }
      for(size_t i=0; i<vecs2.size(); ++i) {
         printf("%4d %9.3f %9.3f %9.3f \n",(int) i,vecs2[i].perp(),vecs2[i].eta(),vecs2[i].phi());
      }

      idx=0;

      for(GenParticleCollection::const_iterator p = p_begin; p != p_end; ++p, ++idx) {
         
         int iMo1 = -1;
         found = find(cands.begin(), cands.end(), p->mother(0));
         if( found != cands.end() ) iMo1 = found - cands.begin();
         int iMo2 = -1;
         found = find(cands.begin(), cands.end(), p->mother(1));
         if( found != cands.end() ) iMo2 = found - cands.begin();
         printf("%4d",idx);
         printf("%7d",p->pdgId());
         printf("%6d",p->status());
         printf("  ");
         printf("%5d",iMo1);
         printf("%5d",iMo2);
/*         printf("%5d",p->mother(1));
         printf("%5d",p->daughter(0));
         printf("%5d",p->daughter(1));*/
         printf("%9.3f",p->pt() );
         printf("%9.3f",p->eta() );
         printf("%9.3f",p->phi() );
         printf("%9.3f",p->energy() );
         printf("\n");

      }



      std::cout << sud[0][0] << " " << sud[0][1] << std::endl;
      std::cout << sud[1][0] << " " << sud[1][1] << std::endl;
//
      std::cout << "**************************" << std::endl;
//
      int js=1;
      pyint1.mint[29]=js;
      pyptisint(&zero,&PT2NOW,&PT2CUT,&pt2,&ifail);
      std::cout << pyint1.vint[399] << " " << pyint1.vint[398] << std::endl;
      pyint1.mint[29]=js;
      pyptisint(&zero,&PT2NOW,&PT2CUT,&pt2,&ifail);
      std::cout << pyint1.vint[399] << " " << pyint1.vint[398] << std::endl;
      pyint1.mint[29]=js;
      pyptisint(&zero,&PT2NOW,&PT2CUT,&pt2,&ifail);
      std::cout << pyint1.vint[399] << " " << pyint1.vint[398] << std::endl;
      std::cout << "--------------------------" << std::endl;
      js=2;
      pyint1.mint[29]=js;
      pyptisint(&zero,&PT2NOW,&PT2CUT,&pt2,&ifail);
      std::cout << pyint1.vint[399] << " " << pyint1.vint[398] << std::endl;
      pyint1.mint[29]=js;
      pyptisint(&zero,&PT2NOW,&PT2CUT,&pt2,&ifail);
      std::cout << pyint1.vint[399] << " " << pyint1.vint[398] << std::endl;
      pyint1.mint[29]=js;
      pyptisint(&zero,&PT2NOW,&PT2CUT,&pt2,&ifail);
      std::cout << pyint1.vint[399] << " " << pyint1.vint[398] << std::endl;

   }

}

// ------------ method called once each job just before starting event loop  ------------
void 
ShowerWeightProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
ShowerWeightProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------

void
ShowerWeightProducer::beginRun(edm::Run& iRun, edm::EventSetup const&)
{
   using namespace edm;
   Handle<LHERunInfoProduct> run;
   bool foundRunInfo = true;
/*   try {
      iRun.getByLabel("source",run);
   } catch (std::exception& ex) {
      std::cout << "lheRuninfo not found " << std::endl;
//      return;
      foundRunInfo = false;
   } */
   foundRunInfo = false;
    

   if( foundRunInfo ) {

   const lhef::HEPRUP thisHeprup_ = run->heprup();


//   std::cout << "HEPRUP \n" << std::endl;
//   std::cout << "IDBMUP " << std::setw(14) << std::fixed << thisHeprup_.IDBMUP.first 
//             << std::setw(14) << std::fixed << thisHeprup_.IDBMUP.second << std::endl; 
   heprup_.idbmup[0] = thisHeprup_.IDBMUP.first;
   heprup_.idbmup[1] = thisHeprup_.IDBMUP.second;
//   std::cout << "EBMUP  " << std::setw(14) << std::fixed << thisHeprup_.EBMUP.first 
//             << std::setw(14) << std::fixed << thisHeprup_.EBMUP.second << std::endl; 
   heprup_.ebmup[0] = thisHeprup_.EBMUP.first;
   heprup_.ebmup[1] = thisHeprup_.EBMUP.second;

//   std::cout << "PDFGUP " << std::setw(14) << std::fixed << thisHeprup_.PDFGUP.first 
//             << std::setw(14) << std::fixed << thisHeprup_.PDFGUP.second << std::endl; 
//   std::cout << "PDFSUP " << std::setw(14) << std::fixed << thisHeprup_.PDFSUP.first 
//             << std::setw(14) << std::fixed << thisHeprup_.PDFSUP.second << std::endl; 
//   std::cout << "IDWTUP " << std::setw(14) << std::fixed << thisHeprup_.IDWTUP << std::endl; 
   heprup_.idwtup = thisHeprup_.IDWTUP;
//   std::cout << "NPRUP  " << std::setw(14) << std::fixed << thisHeprup_.NPRUP << std::endl; 
   heprup_.nprup = thisHeprup_.NPRUP;
/*   std::cout << "        XSECUP " << std::setw(14) << std::fixed 
             << "        XERRUP " << std::setw(14) << std::fixed 
             << "        XMAXUP " << std::setw(14) << std::fixed 
             << "        LPRUP  " << std::setw(14) << std::fixed << std::endl;*/
   for ( unsigned int iSize = 0 ; iSize < thisHeprup_.XSECUP.size() ; iSize++ ) {
/*      std::cout  << std::setw(14) << std::fixed << thisHeprup_.XSECUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.XERRUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.XMAXUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.LPRUP[iSize] 
                 << std::endl;*/
      heprup_.xsecup[iSize] = thisHeprup_.XSECUP[iSize];
      heprup_.xerrup[iSize] = thisHeprup_.XERRUP[iSize];
      heprup_.xmaxup[iSize] = thisHeprup_.XMAXUP[iSize];
      heprup_.lprup[iSize] = thisHeprup_.LPRUP[iSize];
   }
//   std::cout << " " << std::endl;


   headers_const_iterator h_begin = run->headers_begin();
   headers_const_iterator h_end = run->headers_end();

//  std::vector<std::string> header = run->findHeader("MGRunCard");



   for( headers_const_iterator hit = h_begin; hit != h_end; ++hit) {
      size_t found = ((*hit).tag()).find("MGParamCMS");
      if( found != std::string::npos ) {
         for( LHERunInfoProduct::Header::const_iterator lit = (*hit).begin(); lit != (*hit).end(); ++lit) {
            size_t found_cut = (*lit).find(" = qcut");
            if( found_cut != std::string::npos ) {
               std::istringstream ss(  (*lit).substr(0,found_cut) );
               ss >> qCut;
               break;
            }
         }
      }
   }
   } else {
      heprup_.idbmup[0] = 2212;
      heprup_.idbmup[1] = 2212;

      heprup_.ebmup[0] = 4000.0;
      heprup_.ebmup[1] = 4000.0;

      heprup_.idwtup = 3;
//   std::cout << "NPRUP  " << std::setw(14) << std::fixed << thisHeprup_.NPRUP << std::endl; 
      heprup_.nprup = 4;
/*   std::cout << "        XSECUP " << std::setw(14) << std::fixed 
             << "        XERRUP " << std::setw(14) << std::fixed 
             << "        XMAXUP " << std::setw(14) << std::fixed 
             << "        LPRUP  " << std::setw(14) << std::fixed << std::endl;*/
      for ( int iSize = 0 ; iSize < heprup_.nprup ; iSize++ ) {
/*      std::cout  << std::setw(14) << std::fixed << thisHeprup_.XSECUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.XERRUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.XMAXUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.LPRUP[iSize] 
                 << std::endl;*/
         heprup_.xsecup[iSize] = 1.0;
         heprup_.xerrup[iSize] = 0.0;
         heprup_.xmaxup[iSize] = 1.0;
         heprup_.lprup[iSize] =  iSize+1;
      }
//   std::cout << " " << std::endl;



      qCut = 20.0;
      std::cout << "Guessing that qCut = " << qCut << std::endl;
   }   
}

 
// ------------ method called when ending the processing of a run  ------------
/*
void
ShowerWeightProducer::endRun(edm::Run&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
ShowerWeightProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
ShowerWeightProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
ShowerWeightProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(ShowerWeightProducer);
