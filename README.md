activemq-rpm
================

Spec and sources to build activemq 5.7 binary and source rpm.

My starting point was the Puppet Enterprise src rpm located here:

http://yum.puppetlabs.com/enterprise/sources/2.6.0/sources/el/6/SRPMS/pe-activemq-5.6.0-2.pe.el6.src.rpm

I left the original activemq tarball out of the repo. To get it do the following:

    cd SOURCES
    wget http://apache.mirror.nexicom.net/activemq/apache-activemq/5.7.0/apache-activemq-5.7.0-bin.tar.gz

Go to
http://www.apache.org/dyn/closer.cgi?path=%2Factivemq%2Fapache-activemq%2F5.7.0%2Fapache-activemq-5.7.0-bin.tar.gz
to find a mirror closer to you.

To build the source and binary rpm, the rpmbuild tool is necessary

    sudo yum install rpm-build

Some initial rpm configuration may be necessary to build rpm as non
root user.

    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

Once rpmbuild is installed:

    rpmbuild -ba SPECS/activemq.spec

