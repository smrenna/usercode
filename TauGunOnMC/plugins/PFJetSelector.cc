/* \class PFJetSelector
 *
 * Selects a PFJet with a configurable string-based cut.
 * Saves clones of the selected tracks
 *
 * \author: Steven Lowette
 *
 */

#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/SingleObjectSelector.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

typedef SingleObjectSelector<
          reco::PFJetCollection,
          StringCutObjectSelector<reco::PFJet>
        > PFJetSelector;

DEFINE_FWK_MODULE( PFJetSelector );
