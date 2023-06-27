#!/bin/sh
# a simple tool to test the project
# it can be launched even outside tools directory
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
WORKSPACEPATH=`dirname $SCRIPTPATH`
mkdir -pv ${WORKSPACEPATH}/build
cd ${WORKSPACEPATH}/build
cmake ..
make all;
make test; # for gitlab ci, locally use run_all_tests