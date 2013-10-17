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
MECompare(\"$hist1\",\"$hist2\",\"plotGenGluino\"); 
MECompare(\"$hist1\",\"$hist2\",\"plotGenLeptons\");
MECompare(\"$hist1\",\"$hist2\",\"plotGenPart1\");
MECompare(\"$hist1\",\"$hist2\",\"plotGenPart2\");
.q" >> root.sh
root.exe -b < root.sh

psmerge -ocomparisons.PS *.ps
rm *.ps
rename .PS .ps comparisons.PS

date
#---------------------------------------------------------------------------------
