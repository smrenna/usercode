#!/bin/bash
date
source /uscmst1/prod/sw/cms/shrc prod

CMSSW=/uscms_data/d2/mrenna/devel/CMSSW_4_2_3

#basedir=$CMSSW/src/UserCode/SusyAnalysis/SLHAFILES/mSugraScan/m0_m12_10_0_1
basedir=$CMSSW/src/UserCode/SusyAnalysis/SLHAFILES/$SCANDIR

slhas=$basedir/*.slha

i=$OFFSET
t=""
for file in $slhas
do
 if [ $i == $1 ]
 then
   t=$file
   break
 fi
 let 'i = i + 1'
done

INPUTFILE=$t

afile=`python fixname.py $INPUTFILE`
INPUTFILE=${afile/lhe/slha}

workerspace=$PWD

cd $CMSSW/src
eval `scramv1 runtime -sh`
cd $workerspace

flag=$1
myran=$flag
let myran=myran+1
RANDOM=$myran
myran=$RANDOM

echo $myran

configfile=oset_cfg$flag.py

mv oset_cfg.py $configfile

sed -i -e "s,NUMEVTS,$NOEVENTS," $configfile
sed -i -e "s,RUNSLHA,$INPUTFILE," $configfile
sed -i -e "s,SCANDIR,$SCANDIR," $configfile
sed -i -e "s,MYRANSEED,$myran," $configfile

cmsRun $configfile > logfile.out

python << End-Of-Python
import os,sys,string
f=open('logfile.out','r')
g=open('temp.out','w')
vara=""
varb=""
for line in f:
  test=line.find('All included sub')
  if test>-1:
     sl=line.split("I")
     sl[3]=sl[3].replace('D','E')
     vara=float(sl[3])

  test=line.find('Fraction of')
  if test>-1:
     sl=line.split("=")
     sl=sl[1].split()
     varb=1.0-float(sl[0])
f.close()
g.write(" %e  %e \n" % (vara,varb) )
g.close()
End-Of-Python
rm logfile.out

after=""
while read line
do
  after=$line
done < temp.out
rm temp.out
set -- $after
modelname=${afile/.lhe/}
modelstring=$modelname" "$1" "$2
set --
echo $modelstring

python reformatter.py fort.69 "$modelstring"
mv fort.69 $afile

rm *.py
rm fort.69.bak

date
pwd
#---------------------------------------------------------------------------------
