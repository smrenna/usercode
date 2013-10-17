#!/bin/bash
date

suffix="top"

subdir=$1
subdir="noMPI"
subdir=$1

wwwdestination=$PWD

cp ../mkHTML.py .
input=$1
hist1="../run"$suffix$1".root"
hist2="../run"$suffix"0.root"
touch root.sh

echo ".L MECompare.C+ " > root.sh
echo "MECompare(\"$hist1\",\"$hist2\",\"electronPt\"); " >> root.sh
echo "MECompare(\"$hist1\",\"$hist2\",\"photonPt\"); " >> root.sh
echo "MECompare(\"$hist1\",\"$hist2\",\"ePhotonProperties\"); " >> root.sh
echo "MECompare(\"$hist1\",\"$hist2\",\"ePeMProperties\"); " >> root.sh
echo ".q" >> root.sh

root.exe -b < root.sh
#rm root.sh

./mkHTML.py
rename \# '' *.jpg
sed -i -e 's/\#//g' *.html
rm analysis.html
echo "<html>" > analysis.html
echo "<body>" >> analysis.html
echo "<verbatim>" >> analysis.html
diff ../$1.out ../1.out | head -13 >> analysis.html
echo "</verbatim>" >> analysis.html
echo "</body>" >> analysis.html
echo "</html>" >> analysis.html

rm -rf $wwwdestination/$subdir

mkdir $wwwdestination/$subdir

mv *.jpg *.html $wwwdestination/$subdir

date
#---------------------------------------------------------------------------------
