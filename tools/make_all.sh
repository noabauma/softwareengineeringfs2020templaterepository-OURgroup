#!/bin/sh
# a simple tool to make the project
# it can be launched even outside tools directory
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
WORKSPACEPATH=`dirname $SCRIPTPATH`
mkdir -pv ${WORKSPACEPATH}/build
cd ${WORKSPACEPATH}/build
cmake ..
make all