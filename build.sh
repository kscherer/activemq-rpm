#!/bin/bash
if [ ! -f SOURCES/apache-activemq-5.8.0-bin.tar.gz ]; then
    (
        cd SOURCES
        wget https://archive.apache.org/dist/activemq/apache-activemq/5.8.0/apache-activemq-5.8.0-bin.tar.gz
    )
fi

mkdir -p BUILD RPMS SRPMS

rpmbuild -D '%_topdir %(echo $PWD)' -ba SPECS/activemq.spec
