#!/bin/bash
date

wwwdestination=$PWD

hist1="../pythia8_5step.root"
hist2="../bridge_5step.root"
touch root.sh

echo ".L MECompare.C+ " > root.sh
echo "MECompare(\"$hist1\",\"$hist2\",\"plotMHT\"); " >> root.sh
echo "MECompare(\"$hist1\",\"$hist2\",\"plotGenJets\"); " >> root.sh
echo "MECompare(\"$hist1\",\"$hist2\",\"plotEJets\"); " >> root.sh
echo ".q" >> root.sh

root.exe -b < root.sh

./mkHTML.py
rename \# '' *.jpg
sed -i -e 's/\#//g' *.html
rm analysis.html
echo "<html>" > analysis.html
echo "<body>" >> analysis.html
echo "<verbatim>" >> analysis.html
echo "</verbatim>" >> analysis.html
echo "</body>" >> analysis.html
echo "</html>" >> analysis.html


date
#---------------------------------------------------------------------------------
