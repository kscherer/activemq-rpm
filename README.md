activemq-5.6-rpm
================

Spec and sources to build activemq 5.6 binary and source rpm.

My starting point was the Puppet Enterprise src rpm located here:

http://yum.puppetlabs.com/enterprise/sources/2.6.0/sources/el/6/SRPMS/pe-activemq-5.6.0-2.pe.el6.src.rpm

I left the original activemq tarball out of the repo. To get it do the following:

  cd SOURCES
  wget http://www.apache.org/dyn/closer.cgi?path=%2Factivemq%2Fapache-activemq%2F5.6.0%2Fapache-activemq-5.6.0-bin.tar.gz 

To build the source and binary rpm, the rpmbuild tool is necessary

  sudo yum install rpm-build

Once rpmbuild is installed:

  rpmbuild -ba SPECS/activemq.spec

