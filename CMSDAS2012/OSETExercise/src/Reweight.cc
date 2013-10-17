// -*- C++ -*-
//
// Package:    Reweight
// Class:      Reweight
// 
/**\class Reweight Reweight.cc UserCode/Reweight/src/Reweight.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Stephen Mrenna
//         Created:  Mon Jan 10 10:15:43 CST 2011
// $Id: Reweight.cc,v 1.1.1.1 2012/01/10 17:57:48 mrenna Exp $
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

class Reweight : public edm::EDAnalyzer {
   public:
      explicit Reweight(const edm::ParameterSet&);
      ~Reweight();


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      double topDecayWeight(TLorentzVector& t, TLorentzVector& b, TLorentzVector& f, TLorentzVector& fbar);
      double topCorrWeight(int iType, TLorentzVector& p1, TLorentzVector& p2, 
                           TLorentzVector& pt, TLorentzVector& pb, TLorentzVector& peb, TLorentzVector& pne,
                           TLorentzVector& ptb, TLorentzVector& pbb, TLorentzVector& pm, TLorentzVector& pnm);


      // ----------member data ---------------------------

      edm::InputTag src_;

      TH1D* h_p_cosTheta_;
      TH1D* h_p_cosThetap_;
      TH1D* h_m_cosTheta_;
      TH1D* h_m_cosThetap_;
      TH1D* h_p_pT_;
      TH1D* h_m_pT_;
      TH1D* h_p_pTp_;
      TH1D* h_m_pTp_;
      TH1D* h_p_eta_;
      TH1D* h_m_eta_;
      TH1D* h_p_etap_;
      TH1D* h_m_etap_;
      TH1D* h_corr1_;
      TH1D* h_corr2_;
      TH1D* h_corr3_;
      TH1D* h_theta12_raw_;
      TH1D* h_theta12_top_;
      TH1D* h_theta12_ttb_;
      TH1D* h_mass_boson_;

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
Reweight::Reweight(const edm::ParameterSet& iConfig) :
   src_( iConfig.getParameter<edm::InputTag>( "src" ) )
{  
   //now do what ever initialization is needed
   
   edm::Service<TFileService> fs;
   h_p_cosTheta_ = fs->make<TH1D>( "h_p_cosTheta", "Cos[Theta*]", 40, -1.0, 1.0 );
   h_p_cosThetap_ = fs->make<TH1D>( "h_p_cosThetap", "Cos[Theta*] corrected", 40, -1.0, 1.0 );
   h_m_cosTheta_ = fs->make<TH1D>( "h_m_cosTheta", "Cos[Theta*]", 40, -1.0, 1.0 );
   h_m_cosThetap_ = fs->make<TH1D>( "h_m_cosThetap", "Cos[Theta*] corrected", 40, -1.0, 1.0 );

   h_p_pT_ = fs->make<TH1D>( "h_p_pT", "pT(l+) lab", 50, 0.0, 200.0 );
   h_m_pT_ = fs->make<TH1D>( "h_m_pT", "pT(l-) lab", 50, 0.0, 200.0 );
   h_p_pTp_ = fs->make<TH1D>( "h_p_pTp", "pT(l+) lab corrected", 50, 0.0, 200.0 );
   h_m_pTp_ = fs->make<TH1D>( "h_m_pTp", "pT(l-) lab corrected", 50, 0.0, 200.0 );

   h_p_eta_ = fs->make<TH1D>( "h_p_eta", "eta(l+) lab", 50, -2.0, 2.0 );
   h_m_eta_ = fs->make<TH1D>( "h_m_eta", "eta(l-) lab", 50, -2.0, 2.0 );
   h_p_etap_ = fs->make<TH1D>( "h_p_etap", "eta(l+) lab corrected", 50, -2.0, 2.0);
   h_m_etap_ = fs->make<TH1D>( "h_m_etap", "eta(l-) lab corrected", 50, -2.0, 2.0);


   h_corr1_ = fs->make<TH1D>( "h_corr1", "Cos[Theta1*]*Cos[Theta2*]", 40, 0, 3.2 );
   h_corr2_ = fs->make<TH1D>( "h_corr2", "Cos[Theta1*]*Cos[Theta2*]", 40, 0, 3.2 );
   h_corr3_ = fs->make<TH1D>( "h_corr3", "Cos[Theta1*]*Cos[Theta2*]", 40, 0, 3.2 );


   h_theta12_raw_ = fs->make<TH1D>( "h_theta12_raw", "dPhi", 40, 0, 3.2 );
   h_theta12_top_ = fs->make<TH1D>( "h_theta12_top", "dPhi", 40, 0, 3.2 );
   h_theta12_ttb_ = fs->make<TH1D>( "h_theta12_ttb", "dPhi", 40, 0, 3.2 );

   h_mass_boson_ = fs->make<TH1D>( "h_boson_mass", "M(boson) GeV", 40, 60, 100.);




}


Reweight::~Reweight()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
Reweight::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
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



   const Candidate &pIn1= *(pTop->mother(0));
   const Candidate &pIn2= *(pTop->mother(1));

   int iType = ( pIn1.pdgId() == 21 ) ? 1 : 0 ;




   TLorentzVector vpTop = TLorentzVector(pTop->px(),pTop->py(),pTop->pz(),pTop->energy());
   TLorentzVector vpBot = TLorentzVector(pBot->px(),pBot->py(),pBot->pz(),pBot->energy());
   TLorentzVector vpBotLab = vpBot;
   TLorentzVector vmTop = TLorentzVector(mTop->px(),mTop->py(),mTop->pz(),mTop->energy());
   TLorentzVector vmBot = TLorentzVector(mBot->px(),mBot->py(),mBot->pz(),mBot->energy());
   TLorentzVector vmBotLab = vmBot;

   TLorentzVector vIn1 = TLorentzVector(pIn1.px(),pIn1.py(),pIn1.pz(),pIn1.energy());
   TLorentzVector vIn2 = TLorentzVector(pIn2.px(),pIn2.py(),pIn2.pz(),pIn2.energy());


   TLorentzVector vpMu = TLorentzVector(pMu->px(),pMu->py(),pMu->pz(),pMu->energy());
   TLorentzVector vpNu = TLorentzVector(pNu->px(),pNu->py(),pNu->pz(),pNu->energy());
   TLorentzVector vmMu = TLorentzVector(mMu->px(),mMu->py(),mMu->pz(),mMu->energy());
   TLorentzVector vmNu = TLorentzVector(mNu->px(),mNu->py(),mNu->pz(),mNu->energy());

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


   double corrWeight = topCorrWeight(iType, vIn1, vIn2, vpTop, vpBot, vpMu, vpNu, vmTop, vmBot, vmMu, vmNu );



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
   h_p_pT_ -> Fill( vpMuLab.Pt() );
   h_m_pT_ -> Fill( vmMuLab.Pt() );
   h_p_eta_ -> Fill( vpMuLab.Eta() );
   h_m_eta_ -> Fill( vmMuLab.Eta() );

   double newWeight_p = topDecayWeight(vpTop, vpBot, vpNu, vpMu );
   double newWeight_m = topDecayWeight(vmTop, vmBot, vmNu, vmMu );

   double newWeight = newWeight_p * newWeight_m;

   if( pBoson->pdgId() == 24 ) newWeight=1.0;
   h_mass_boson_ -> Fill(vpBoson.M(),newWeight);
   h_mass_boson_ -> Fill(vmBoson.M(),newWeight);

   h_p_cosThetap_->Fill(cos(pAngle),newWeight);
   h_m_cosThetap_->Fill(cos(mAngle),newWeight);
   h_p_pTp_ -> Fill( vpMuLab.Pt(),newWeight );
   h_m_pTp_ -> Fill( vmMuLab.Pt(),newWeight );
   h_p_etap_ -> Fill( vpMuLab.Eta(),newWeight );
   h_m_etap_ -> Fill( vmMuLab.Eta(),newWeight );


   TVector3 vPair = -(vpTopLab+vmTopLab).BoostVector();

   if( (vpTopLab+vmTopLab).M() < 400.0 ) {


   double pmangle = fabs(vpMuLab.Phi()-vmMuLab.Phi());
   pmangle = ( pmangle > M_PI ) ? 2*M_PI - pmangle : pmangle ;
   h_theta12_raw_->Fill(pmangle);
   h_theta12_top_->Fill(pmangle, newWeight);
   h_theta12_ttb_->Fill(pmangle, newWeight* corrWeight);


   }

   vpMuLab.Boost(vPair);
   vmMuLab.Boost(vPair);
   vpTopLab.Boost(vPair);
   vmTopLab.Boost(vPair);

   vpNuLab.Boost(vPair);
   vmNuLab.Boost(vPair);
   vpBotLab.Boost(vPair);
   vmBotLab.Boost(vPair);



   if( (vpTopLab+vmTopLab).M() < 400.0 ) {

   double ppAngle = vpMuLab.Phi();
   double mmAngle = vmMuLab.Phi();

   double Observable = fabs(ppAngle-mmAngle);
   Observable = ( Observable> M_PI) ? 2*M_PI - Observable : Observable;

   h_corr1_ -> Fill( Observable );
   h_corr2_ -> Fill( Observable , newWeight );
   h_corr3_ -> Fill( Observable , newWeight*corrWeight );

   }

}


// ------------ method called once each job just before starting event loop  ------------
void 
Reweight::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
Reweight::endJob() {
}


double
Reweight::topDecayWeight(TLorentzVector& t, TLorentzVector& b, TLorentzVector& f, TLorentzVector& fbar) {
//C...Angular correlation in f -> f' + W -> f' + 2 quarks/leptons.
/*        I1=IREF(IP,8)
        IF(MOD(KFAGM,2).EQ.0) THEN
          I2=N+1
          I3=N+2
        ELSE
          I2=N+2
          I3=N+1
        ENDIF
        I4=IREF(IP,2) */
   TLorentzVector wBoson = f + fbar;
   double wt = t.Dot( fbar ) * b.Dot( f );
   double mtop2 = t.M2();
   double mw2   = wBoson.M2();
   double wtmax = (mtop2*mtop2-mw2*mw2)/8.0;
/*        WT=(P(I1,4)*P(I2,4)-P(I1,1)*P(I2,1)-P(I1,2)*P(I2,2)-
     &  P(I1,3)*P(I2,3))*(P(I3,4)*P(I4,4)-P(I3,1)*P(I4,1)-
     &  P(I3,2)*P(I4,2)-P(I3,3)*P(I4,3))
     WTMAX=(P(I1,5)**4-P(IREF(IP,1),5)**4)/8D0*/

   return wt/wtmax;
}

double
Reweight::topCorrWeight(int iType, TLorentzVector& p1, TLorentzVector& p2, 
                        TLorentzVector& pt, TLorentzVector& pb, TLorentzVector& peb, TLorentzVector& pne,
                        TLorentzVector& ptb, TLorentzVector& pbb, TLorentzVector& pm, TLorentzVector& pnm) {
   const double m_t2=175.*175.;
   const double kappa=1.0;
//   double dbpnp=pb.Dot(pne);
//   double dbana=pbb.Dot(pnm);
   double dtpla=pt.Dot(peb);
   double dtplp=pt.Dot(pm);
   double dtala=ptb.Dot(peb);
   double dtalp=ptb.Dot(pm);
   double dp1p2=p1.Dot(p2);
   double dlpla=peb.Dot(pm);
   double dp1tp=p1.Dot(pt);
   double dp2tp=p2.Dot(pt);
   double dtpta=pt.Dot(ptb);
   double dp1lp=p1.Dot(pm);
   double dp1la=p1.Dot(peb);
   double dp2lp=p2.Dot(pm);
   double dp2la=p2.Dot(peb);

/*   double dp1tp=-p1.Dot(pt);
   double dp2tp=-p2.Dot(pt);
   double dtpta=pt.Dot(ptb);
   double dp1lp=-p1.Dot(pm);
   double dp1la=-p1.Dot(peb);
   double dp2lp=-p2.Dot(pm);
   double dp2la=-p2.Dot(peb); */



//   std::cout << pt.M() << " " << ptb.M() << " " << m_t2 << std::endl;
//   std::cout << (p1+p2).M() << " " << (pt+ptb).M() << std::endl;
    
   double ratio=1.0;

   if( iType==0 ) {

     double qqb_corr=
        (   2.0*dtpla*dtalp*( dp1tp*dp1tp + dp2tp*dp2tp )
              - ( dtplp*dtpla + dtalp*dtala )*dp1p2*m_t2
              - dlpla*(2.0*dp1tp*dp2tp - m_t2*dp1p2)*m_t2
              + 2.0*(dp1tp*dp1lp*dp2la + dp2tp*dp1la*dp2lp)*m_t2  ) ;

     double qqb_uncorr=dtpla*dtalp *( pow(dp1tp,2) + pow(dp2tp,2) + m_t2*dp1p2) ;

//     double qqb=(1.0-kappa)*qqb_uncorr+kappa*qqb_corr;

     ratio = (1.0-kappa) + kappa*qqb_corr/qqb_uncorr;

//     std::cout << " iType=0 " << qqb_corr << " " << qqb_uncorr << " " << ratio << std::endl;



   } else {


      double gg_unlike_corr=
         ((2.0*(2.0*dp1tp*dp2tp-m_t2*dp1p2))/ pow(dp1p2,2))
         *(   2.0*dtpla*dtalp*( pow(dp1tp,2) + pow(dp2tp,2) )
              -(dtplp*dtpla+dtalp*dtala)*dp1p2*m_t2
             -dlpla*(2.0*dp1tp*dp2tp-m_t2*dp1p2)*m_t2
              +2.0*(dp1tp*dp1lp*dp2la+dp2tp*dp1la*dp2lp)*m_t2  ) ;

      double  gg_unlike_uncorr= dtpla*dtalp
         *((2.0*(2.0*dp1tp*dp2tp-m_t2*dp1p2)) / pow(dp1p2,2) )
         *( pow(dp1tp,2) + pow(dp2tp,2) +m_t2*dp1p2);

//      double gg_unlike=(1.0-kappa)*gg_unlike_uncorr+kappa*gg_unlike_corr;

      double gg_like_corr= 2.0*m_t2*m_t2*(dtalp*dtala+dtplp*dtpla-m_t2*dlpla);

      double gg_like_uncorr=dtpla*dtalp*2.0*m_t2*dtpta;

//      double gg_like=(1.0-kappa)*gg_like_uncorr+kappa*gg_like_corr;

//      double gg_full= (1.0-kappa)*(gg_like_uncorr+gg_unlike_uncorr) + kappa*(gg_like_corr+gg_unlike_corr) ;

      ratio = (1.0-kappa) + kappa*(gg_like_corr+gg_unlike_corr)/
       (gg_like_uncorr+gg_unlike_uncorr);

//     std::cout << " iType=1 " << gg_like_corr+gg_unlike_corr << " " << gg_like_uncorr+gg_unlike_uncorr << " " << ratio << std::endl;

   }
   
   return ratio;
}

//define this as a plug-in
DEFINE_FWK_MODULE(Reweight);
