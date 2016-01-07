#!/bin/bash
date

hist1=$1
hist2=$2
echo $hist1
echo $hist2

rm root.sh
touch root.sh
rm *.ps

echo "
.L MECompare.C+ 
MECompare(\"$hist1\",\"$hist2\",\"plotGenWBoson\"); 
MECompare(\"$hist1\",\"$hist2\",\"plotTransverseW\"); 
MECompare(\"$hist1\",\"$hist2\",\"plotGenLeptons\");
MECompare(\"$hist1\",\"$hist2\",\"plotGenJets\");
MECompare(\"$hist1\",\"$hist2\",\"plotLeptonPlusJet\");
MECompare(\"$hist1\",\"$hist2\",\"plotChargedTracks\"); 
.q" >> root.sh
root -b -l < root.sh

gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=comparisons.PS *.ps
rm *.ps
rename .PS .ps comparisons.PS

date
#---------------------------------------------------------------------------------
