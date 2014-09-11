activemq-rpm
================

Spec and sources to build activemq 5.9.1 binary and source rpm.

My starting point was the Puppet Lab ActiveMQ 5.8.0 src rpm located here:

http://yum.puppetlabs.com/el/6.5/dependencies/SRPMS/activemq-5.8.0-3.el6.src.rpm

I then applied the 5.9.1 patches from Jo Rhett. Thank you!

http://www.netconsonance.com/2014/06/updated-activemq-5-9-1-2-rpm-with-rest-apis/

To build the source and binary rpm, the rpmbuild tool is necessary

    sudo yum install rpm-build

To build rpm run the provided build.sh script. It will download the
activemq tarball from the Apache archive and build it.
