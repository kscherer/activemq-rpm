activemq-rpm
================

Spec and sources to build activemq 5.8 binary and source rpm.

My starting point was the Puppet Lab ActiveMQ src rpm located here:

http://yum.puppetlabs.com/el/6.5/dependencies/SRPMS/activemq-5.8.0-3.el6.src.rpm

To build the source and binary rpm, the rpmbuild tool is necessary

    sudo yum install rpm-build

To build rpm run the provided build.sh script. It will download the
activemq tarball from the Apache archive and build it.
