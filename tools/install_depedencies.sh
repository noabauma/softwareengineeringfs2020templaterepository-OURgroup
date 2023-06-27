#!/bin/sh
INSTALL_FUNCTION='apt-get -y install'

PACKAGES= ''
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
WORKSPACEPATH=`dirname $SCRIPTPATH`

# install all packages inside depedencies.txt
cat ${WORKSPACEPATH}/.depedencies.txt | xargs ${INSTALL_FUNCTION}
# update(download) submodules
git submodule update --init --recursive