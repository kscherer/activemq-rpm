#!/bin/bash
if [ ! -f SOURCES/apache-activemq-5.9.1-bin.tar.gz ]; then
    (
        cd SOURCES
        wget http://apache.mirror.nexicom.net/activemq/5.9.1/apache-activemq-5.9.1-bin.tar.gz
    )
fi

mkdir -p BUILD RPMS SRPMS

rpmbuild -D '%_topdir %(echo $PWD)' -ba SPECS/activemq.spec
