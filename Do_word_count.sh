#!/bin/bash
LCGVERSION=88
LCGEXTERNALS='--ext scipy --ext matplotlib --ext scikitlearn'
SETUP="lb-run ${LCGEXTERNALS} LCG/${LCGVERSION}"
PREFIX=${HOME}/Thesis/Thesis
LOGFILE=${PREFIX}/wordcounts.log

echo 'Loading group login'
#. /cvmfs/lhcb.cern.ch/group_login.sh > ${LOGFILE} 2>&1
. /cvmfs/lhcb.cern.ch/group_login.sh | tee ${LOGFILE}
#. /afs/cern.ch/lhcb/software/releases/LBSCRIPTS/prod/InstallArea/scripts/LbLogin.sh > ${LOGFILE} 2>&1
#for name in willF chris lydia kathryn stephenD
#do
#  curl -o ${PREFIX}/wordcount_${name}.txt http://www-pnp.physics.ox.ac.uk/~lupton/wordcount_${name}.txt >> ${LOGFILE} 2>&1
#done
echo 'Doing Python script'
#echo "${SETUP} python ${PREFIX}/wordcount.py >> ${LOGFILE} 2>&1"
#${SETUP} python ${PREFIX}/wordcount.py >> ${LOGFILE} 2>&1

echo ${SETUP} python ${PREFIX}/wordcount.py | tee -a ${LOGFILE}
${SETUP} python ${PREFIX}/wordcount.py | tee -a ${LOGFILE}


#eos root://eosuser.cern.ch cp ${PREFIX}/thebigrace.pdf /eos/user/o/olupton/www/ >> ${LOGFILE} 2>&1
#${SETUP} python ${PREFIX}/wordcounts.py toprint >> ${LOGFILE} 2>&1
#eos root://eosuser.cern.ch cp ${PREFIX}/thebigrace.pdf /eos/user/o/olupton/www/thebigraceresults.pdf >> ${LOGFILE} 2>&1
