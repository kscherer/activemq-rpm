activemq-rpm
================

Spec and sources to build activemq 5.7 binary and source rpm.

My starting point was the Puppet Enterprise src rpm located here:

http://yum.puppetlabs.com/enterprise/sources/2.6.0/sources/el/6/SRPMS/pe-activemq-5.6.0-2.pe.el6.src.rpm

To build the source and binary rpm, the rpmbuild tool is necessary

    sudo yum install rpm-build

To build rpm run the provided build.sh script. It will download the
activemq tarball from the Apache archive and build it.
