#!/bin/bash

##
## This file is for running tox, coverage test
##
## Jenkins tox or coverage test job will use this file on Jenkins slave server.
## The job name is "NECCSPortal-dashboard_xxx_Tox" or "NECCSPortal-dashboard_xxx_Coverage"
##
## NECCSPortal-dashboard is not plugin of Horizon.
## The way of running tox test of NECCSPortal-dashboard is a little bit special.
## So we write the code that way in this file.
##

##
## Variables determined by Jenkins
if [ "${WORKSPACE}" = "" ]; then
  echo "You need to export WORKSPACE env"
  exit 1
fi
if [ "${BUILD_NUMBER}" = "" ]; then
  echo "You need to export BUILD_NUMBER env"
  exit 1
fi
if [ "${GITHUB_BK_DIR}" = "" ]; then
  echo "You need to export GITHUB_BK_DIR env"
  exit 1
fi
if [ "${WITH_COVERAGE}" = "" ]; then
  echo "You need to export WITH_COVERAGE env"
  exit 1
fi
if [ "${TARGET_HORIZON_BR}" = "" ]; then
  echo "You need to export TARGET_HORIZON_BR env"
  exit 1
fi
TARGET_HORIZON_BR_NM=${TARGET_HORIZON_BR//\//_}


##
## RPMs
yum install -y gcc libffi-devel openssl-devel

##
## Git clone Openstack/horizon
cd ${GITHUB_BK_DIR}

if ls ${GITHUB_BK_DIR}/horizon.${TARGET_HORIZON_BR_NM} > /dev/null 2>&1
then
  echo "Already github source is cloned"
else
  git clone -b ${TARGET_HORIZON_BR} --single-branch https://github.com/openstack/horizon.git
  mv horizon horizon.${TARGET_HORIZON_BR_NM}
fi
cd horizon.${TARGET_HORIZON_BR_NM}
git pull
git log -n 1 --format=%H

##
## Create temporary directory
mkdir ${WORKSPACE}/tox_temp_${BUILD_NUMBER}
cd ${WORKSPACE}/tox_temp_${BUILD_NUMBER}
cp -prf ${GITHUB_BK_DIR}/horizon.${TARGET_HORIZON_BR_NM} ${WORKSPACE}/tox_temp_${BUILD_NUMBER}/horizon


##
## Put NECCSPortal-dashboard to horizon
cd ${WORKSPACE}/../
rsync -a ${WORKSPACE}/* ${WORKSPACE}/tox_temp_${BUILD_NUMBER}/horizon/ --exclude tox_temp_${BUILD_NUMBER}


##
## Run tox/coverage
cd ${WORKSPACE}/tox_temp_${BUILD_NUMBER}/horizon/
if [ "${WITH_COVERAGE}" = "yes" ]; then
  ./run_tests.sh -V -c -n
  cp -p coverage.xml ${WORKSPACE}/
else
  ./run_tests.sh -V nec_portal
fi

echo "bye"
