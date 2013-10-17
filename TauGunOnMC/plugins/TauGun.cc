
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "GeneratorInterface/ExternalDecays/interface/DecayRandomEngine.h"

#include "HepMC/GenEvent.h"
#include "HepMC/IO_HEPEVT.h"
#include "GeneratorInterface/Pythia6Interface/interface/Pythia6Service.h"
#include "GeneratorInterface/Pythia6Interface/interface/Pythia6Declarations.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "GeneratorInterface/ExternalDecays/interface/TauolaInterface.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"


CLHEP::HepRandomEngine* decayRandomEngine;


class TauGun : public edm::EDProducer {

  public:

    TauGun( const edm::ParameterSet& );
    virtual ~TauGun();
    void beginJob();
    void endJob();
    void beginRun( edm::Run &, edm::EventSetup const & );
    void endRun( edm::Run &, edm::EventSetup const & );
    void produce( edm::Event &, const edm::EventSetup & ) ;
      
  private:

    void attachPy6DecaysToGenEvent(int);
    void generateEvent(const edm::View<reco::Candidate> &v);

    gen::Pythia6Service * fPy6Service;
    HepMC::GenEvent * fEvt;
    gen::TauolaInterface * tauola;

    edm::InputTag seedSrc_, vtxSrc_, genSrc_;
    bool fixedSeed_, genSeed_;
    double charge_, eta_, phi_, e_, vx_, vy_, vz_;
    bool fHepMCVerbosity;
    int  fPylistVerbosity;
    int  fMaxEventsToPrint;
    bool useTauola_;

};


TauGun::TauGun(const edm::ParameterSet & pset) :
  fPy6Service( new gen::Pythia6Service(pset) ),
  fEvt(0)
{

  fHepMCVerbosity   = pset.getUntrackedParameter<bool>("pythiaHepMCVerbosity", false ) ;
  fPylistVerbosity  = pset.getUntrackedParameter<int>( "pythiaPylistVerbosity", 0 ) ;
  fMaxEventsToPrint = pset.getUntrackedParameter<int>( "maxEventsToPrint", 0 );

  // Turn off banner printout
  if (!gen::call_pygive("MSTU(12)=12345")) {
    throw edm::Exception(edm::errors::Configuration, "PythiaError")
      <<" pythia did not accept MSTU(12)=12345";
  }

  produces<edm::HepMCProduct>();

  seedSrc_   = pset.getParameter<edm::InputTag>("SeedSrc");
  vtxSrc_    = pset.getParameter<edm::InputTag>("VtxSrc");
  genSrc_    = pset.getParameter<edm::InputTag>("GenSrc");
  genSeed_   = pset.getParameter<bool>("GenSeed");
  fixedSeed_ = pset.getParameter<bool>("FixedSeed");
  charge_    = pset.getParameter<int>("FixedCharge"); // should be 1 or -1
  eta_       = pset.getParameter<double>("FixedEta");
  phi_       = pset.getParameter<double>("FixedPhi");
  e_         = pset.getParameter<double>("FixedEnergy");
  vx_        = pset.getParameter<double>("FixedVtxX");
  vy_        = pset.getParameter<double>("FixedVtxY");
  vz_        = pset.getParameter<double>("FixedVtxZ");
  useTauola_ = pset.getParameter<bool>("UseTauola");

  edm::Service<edm::RandomNumberGenerator> rng;
  if(!rng.isAvailable()) {
     throw cms::Exception("Configuration")
     << "The RandomNumberProducer module requires the RandomNumberGeneratorService\n"
        "which appears to be absent.  Please add that service to your configuration\n"
        "or remove the modules that require it." << std::endl;
  } 
  decayRandomEngine = &rng->getEngine();   
  if (useTauola_) tauola = new gen::TauolaInterface(pset);
}


TauGun::~TauGun() {
  if (useTauola_ && tauola) delete tauola;
}


void TauGun::beginJob() {

  { // make the Py6Service go out of scope before tauola
    assert ( fPy6Service ) ;

    gen::Pythia6Service::InstanceWrapper guard(fPy6Service);  // grab Py6 instance

    fPy6Service->setGeneralParams();
    fPy6Service->setCSAParams();
    fPy6Service->setSLHAParams();

    // std::cout << " FYI: MSTU(10)=1 is ENFORCED in Py6-PGuns, for technical reasons" << std::endl;
    gen::call_pygive("MSTU(10)=1"); // particle mass setting

    call_pyinit("NONE", "", "", 0.0);
  }

}

void TauGun::endJob() {
  if (useTauola_) tauola->statistics();
  call_pystat(1);
}


void TauGun::beginRun(edm::Run & r, edm::EventSetup const & es) {
  if (useTauola_) tauola->init(es);
}


void TauGun::endRun(edm::Run & r, edm::EventSetup const & es) {
}


void TauGun::produce(edm::Event & evt, const edm::EventSetup & es) {

/*  if (!fixedSeed_ && !genSeed_) {
    edm::Handle<edm::View<reco::Candidate> > seeds;
    evt.getByLabel(seedSrc_, seeds);
    // assume there's only one
//    charge_    = (*seeds)[0].charge();
    charge_    = (*seeds)[0].qx3();
    eta_       = (*seeds)[0].eta();
    phi_       = (*seeds)[0].phi();
    e_         = (*seeds)[0].energy();
    edm::Handle<std::vector<reco::Vertex> > vtxs;
    evt.getByLabel(vtxSrc_, vtxs);
    // assume the first one is the good one
    vx_        = (*vtxs)[0].x();
    vy_        = (*vtxs)[0].y();
    vz_        = (*vtxs)[0].z();
    }*/
//  if (genSeed_) {
    edm::Handle<edm::View<reco::Candidate> > genparts;
    evt.getByLabel(genSrc_, genparts);
    const edm::View<reco::Candidate> &genCollect = *genparts;
    for (unsigned int iPtcl = 0; iPtcl < genparts->size(); ++iPtcl) {
      const reco::Candidate & particle = (*genparts)[iPtcl];
      if (particle.status() == 3 && std::abs(particle.pdgId()) == 15) {
        // assume there's only one
        charge_    = particle.charge();
        eta_       = particle.eta();
        phi_       = particle.phi();
        e_         = particle.energy();
        vx_        = particle.vx();
        vy_        = particle.vy();
        vz_        = particle.vz();
      }
    }
//    }


  // shoot the gun and create the tau and neutrino
  generateEvent(genCollect) ;

  // run tauola (needs the presence of the neutrino)
  if (useTauola_) fEvt = tauola->decay(fEvt);

//  fEvt->print();
//  call_pylist(fPylistVerbosity);

  // now switch to Pythia
  HepMC::IO_HEPEVT conv;
  gen::Pythia6Service::InstanceWrapper guard(fPy6Service);

  // write the HEPEVT record into the PYJETS common block, so that we can decay
  call_pyhepc(2);  
  // record the number of good entries so far
  int nrtopreserve = pyjets.n;
  // now let Pythia find further particles to decay
  gen::pyexec_();

  // add the new daughters into the HepMC fEvt record
  attachPy6DecaysToGenEvent(nrtopreserve);

  // final additions
  fEvt->set_beam_particles(0,0);
  fEvt->set_event_number(evt.id().event());
  fEvt->set_signal_process_id(pypars.msti[0]) ;  

  int evtN = evt.id().event();
  if ( evtN <= fMaxEventsToPrint ) {
    if ( fPylistVerbosity ) call_pylist(fPylistVerbosity);
    if ( fHepMCVerbosity ) if ( fEvt ) fEvt->print();
  }
   
  std::auto_ptr<edm::HepMCProduct> bare_product(new edm::HepMCProduct());  
  if (fEvt) bare_product->addHepMCData( fEvt );
  evt.put(bare_product);

}


void TauGun::generateEvent(const edm::View<reco::Candidate> &genparts) {
   
  double theta  = 2.*atan(exp(-eta_));

  // grab Py6 instance
  HepMC::IO_HEPEVT conv;
  gen::Pythia6Service::InstanceWrapper guard(fPy6Service);

  // here re-create fEvt
  fEvt = new HepMC::GenEvent() ;
  HepMC::GenVertex * vtx = new HepMC::GenVertex(HepMC::FourVector(10*vx_,10*vy_,10*vz_)); // scale to mm
  int ip = 0, py6PID = 0;
  double energy = 0, neutrenergy = e_;
  HepMC::FourVector p;
  HepMC::GenParticle * part = 0;
  HepMC::Polarization pol;

//  const reco::GenParticle & seeds = (*genparts)[0]+(*genparts)[1];

  // add the W
  ++ip;

  charge_ = genparts[0].charge();
  py6PID = 24*charge_; // W+ -> 24 ; H+ -> 37
//  energy = e_ + neutrenergy;
  // add to the pythia event record
//  pyjets.p[4][ip-1] = 1;//gen::pymass_(py6PID);
//  gen::py1ent_(ip, py6PID, energy, theta, phi_);
  pyjets.k[0][ip-1] = 2;
  pyjets.k[1][ip-1] = py6PID;
  pyjets.k[2][ip-1] = 0;
  pyjets.k[3][ip-1] = 2; // set first daughter
  pyjets.k[4][ip-1] = 3; // set last daughter
  // add to the HepMC event
  p = HepMC::FourVector(genparts[0].px()+genparts[1].px(),genparts[0].py()+genparts[1].py(),
                        genparts[0].pz()+genparts[1].pz(),genparts[0].energy()+genparts[1].energy());
  pyjets.p[0][ip-1] = p.px();
  pyjets.p[1][ip-1] = p.py();
  pyjets.p[2][ip-1] = p.pz();
  pyjets.p[3][ip-1] = p.e();
  pyjets.p[4][ip-1] = p.m();
//  p = HepMC::FourVector(pyjets.p[0][ip-1], pyjets.p[1][ip-1], pyjets.p[2][ip-1], energy);
  part = new HepMC::GenParticle(p, py6PID, 2);
//  pol = HepMC::Polarization(M_PI/2 *(1 + charge_), 0);
//  part->set_polarization(pol);
  part->suggest_barcode(ip);
  vtx->add_particle_in(part);

  // add the tau
  ++ip;
  py6PID = -15*charge_; // tau
  energy = e_;
  // add to the pythia event record
  pyjets.p[4][ip-1] = gen::pymass_(py6PID);
  gen::py1ent_(ip, py6PID, energy, theta, phi_);
  pyjets.k[2][ip-1] = 1; // set parent
  pyjets.k[0][ip-1] = 1;
  pyjets.k[1][ip-1] = genparts[0].pdgId();
  pyjets.k[2][ip-1] = 1;
  pyjets.k[3][ip-1] = 0; // set first daughter
  pyjets.k[4][ip-1] = 0; // set last daughter
  // add to the HepMC event
//  p = HepMC::FourVector(pyjets.p[0][ip-1], pyjets.p[1][ip-1], pyjets.p[2][ip-1], energy);
  p = HepMC::FourVector(genparts[0].px(),genparts[0].py(),genparts[0].pz(),genparts[0].energy());
  pyjets.p[0][ip-1] = p.px();
  pyjets.p[1][ip-1] = p.py();
  pyjets.p[2][ip-1] = p.pz();
  pyjets.p[3][ip-1] = p.e();
  pyjets.p[4][ip-1] = p.m();
  part = new HepMC::GenParticle(p, genparts[0].pdgId(), 1);
//  pol = HepMC::Polarization(M_PI/2 *(1 + charge_), 0);
//  part->set_polarization(pol);
  part->suggest_barcode(ip);
  vtx->add_particle_out(part);

  // add the neutrino
  ++ip;
  py6PID = +16*charge_; // neutrino
  energy = neutrenergy;
  // add to the pythia event record
  pyjets.p[4][ip-1] = 0; // set mass
  gen::py1ent_(ip, py6PID, energy, theta, phi_);
  pyjets.k[2][ip-1] = 1; // set parent
  // add to the HepMC event
//  p = HepMC::FourVector(pyjets.p[0][ip-1], pyjets.p[1][ip-1], pyjets.p[2][ip-1], energy);
  p = HepMC::FourVector(genparts[1].px(),genparts[1].py(),genparts[1].pz(),genparts[1].energy());
  pyjets.p[0][ip-1] = p.px();
  pyjets.p[1][ip-1] = p.py();
  pyjets.p[2][ip-1] = p.pz();
  pyjets.p[3][ip-1] = p.e();
  pyjets.p[3][ip-1] = p.m();
  pyjets.k[0][ip-1] = genparts[1].status();
  pyjets.k[1][ip-1] = genparts[1].pdgId();
  pyjets.k[2][ip-1] = 1;
  pyjets.k[3][ip-1] = 0; // set first daughter
  pyjets.k[4][ip-1] = 0; // set last daughter
  part = new HepMC::GenParticle(p, genparts[1].pdgId(), 1);
//  pol = HepMC::Polarization(M_PI/2 *(1 + charge_), 0);
//  part->set_polarization(pol);
  part->suggest_barcode(ip);
  vtx->add_particle_out(part);

  // construct the event
  fEvt->add_vertex(vtx);
  //fEvt->print();

  // write the HEPEVT record into the PYJETS common block, so that we can decay
  conv.write_event( fEvt ) ;

}


void TauGun::attachPy6DecaysToGenEvent(int nrtopreserve)
{

   for ( int iprt=nrtopreserve; iprt<pyjets.n; iprt++ ) // the pointer is shifted by -1, c++ style
   {
      int parent = pyjets.k[2][iprt];
      if ( parent != 0 )
      {
         // pull up parent particle
         //
         HepMC::GenParticle* parentPart = fEvt->barcode_to_particle( parent );
         parentPart->set_status( 2 ); // reset status, to mark that it's decayed
         
         HepMC::GenVertex* DecVtx = new HepMC::GenVertex(
           // need to add in the starting vertex and scale to mm
           HepMC::FourVector(pyjets.v[0][iprt]+10*vx_,
                             pyjets.v[1][iprt]+10*vy_,
                             pyjets.v[2][iprt]+10*vz_,
                             pyjets.v[3][iprt])
         );

         DecVtx->add_particle_in( parentPart ); // this will cleanup end_vertex if exists,
                                                // and replace with the new one
                                                // I presume barcode will be given automatically
         
         HepMC::FourVector  pmom(pyjets.p[0][iprt],pyjets.p[1][iprt],
                                 pyjets.p[2][iprt],pyjets.p[3][iprt] );
         
         int dstatus = 0;
         if ( pyjets.k[0][iprt] >= 1 && pyjets.k[0][iprt] <= 10 )  
         {
            dstatus = 1;
         }
         else if ( pyjets.k[0][iprt] >= 11 && pyjets.k[0][iprt] <= 20 ) 
         {
            dstatus = 2;
         }
         else if ( pyjets.k[0][iprt] >= 21 && pyjets.k[0][iprt] <= 30 ) 
         {
            dstatus = 3;
         }
         else if ( pyjets.k[0][iprt] >= 31 && pyjets.k[0][iprt] <= 100 )
         {
            dstatus = pyjets.k[0][iprt];
         }
         HepMC::GenParticle* daughter = 
            new HepMC::GenParticle(pmom,
                                   HepPID::translatePythiatoPDT( pyjets.k[1][iprt] ),
                                   dstatus);
         daughter->suggest_barcode( iprt+1 );
         DecVtx->add_particle_out( daughter );
         // give particle barcode as well !

         int iprt1;
         for ( iprt1=iprt+1; iprt1<pyjets.n; iprt1++ ) // the pointer is shifted by -1, c++ style
         {
            if ( pyjets.k[2][iprt1] != parent ) break; // another parent particle, break the loop

            HepMC::FourVector  pmomN(pyjets.p[0][iprt1],pyjets.p[1][iprt1],
                                     pyjets.p[2][iprt1],pyjets.p[3][iprt1] );

            dstatus = 0;
            if ( pyjets.k[0][iprt1] >= 1 && pyjets.k[0][iprt1] <= 10 )  
            {
               dstatus = 1;
            }
            else if ( pyjets.k[0][iprt1] >= 11 && pyjets.k[0][iprt1] <= 20 ) 
            {
               dstatus = 2;
            }
            else if ( pyjets.k[0][iprt1] >= 21 && pyjets.k[0][iprt1] <= 30 ) 
            {
               dstatus = 3;
            }
            else if ( pyjets.k[0][iprt1] >= 31 && pyjets.k[0][iprt1] <= 100 )
            {
               dstatus = pyjets.k[0][iprt1];
            }
            HepMC::GenParticle* daughterN = 
               new HepMC::GenParticle(pmomN,
                                      HepPID::translatePythiatoPDT( pyjets.k[1][iprt1] ),
                                      dstatus);
            daughterN->suggest_barcode( iprt1+1 );
            DecVtx->add_particle_out( daughterN );           
         }
         
         iprt = iprt1-1; // reset counter such that it doesn't go over the same child more than once
                         // don't forget to offset back into c++ counting, as it's already +1 forward

         fEvt->add_vertex( DecVtx );

      }
   }

   return;

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(TauGun);
