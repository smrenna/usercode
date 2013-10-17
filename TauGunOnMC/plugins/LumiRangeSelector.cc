
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


class LumiRangeSelector : public edm::EDFilter {

  public:

    explicit LumiRangeSelector(const edm::ParameterSet & iConfig);
    ~LumiRangeSelector() {}

  private:

    virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);
    
    unsigned int run_;
    std::vector<unsigned int> lumimin_, lumimax_;

};


LumiRangeSelector::LumiRangeSelector(const edm::ParameterSet & iConfig) {
  run_ = iConfig.getParameter<unsigned int>("RunNr");
  lumimin_ = iConfig.getParameter<std::vector<unsigned int> >("LumiMin");
  lumimax_ = iConfig.getParameter<std::vector<unsigned int> >("LumiMax");
}


bool LumiRangeSelector::filter(edm::Event & iEvent, const edm::EventSetup & iSetup) {

  if (iEvent.id().run() != run_) return false;

  bool result = false;
  for (unsigned int i = 0; i < std::min(lumimin_.size(),lumimax_.size()); ++i) {
    result = result or (iEvent.luminosityBlock() >= lumimin_.at(i) &&
                        iEvent.luminosityBlock() <= lumimax_.at(i));
  }
  return result;

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(LumiRangeSelector);
