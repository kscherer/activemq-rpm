%global _name          activemq
%global _version       5.8.0
%global _prefix /usr/share

Summary: Apache ActiveMQ
Name: %{_name}
Version: %{_version}
Release: 1%{?dist}
License: ASL 2.0
Group: System Environment/Daemons
URL: http://activemq.apache.org/
Source0: http://www.apache.org/dist//activemq/apache-activemq/%{version}/apache-activemq-%{version}-bin.tar.gz
Source1: activemq.init.rh
Source2: activemq.xml
Source3: activemq.log4j.properties
Source4: activemq.jetty.xml
Source5: activemq.credentials.properties
Source6: activemq.jetty-realm.properties
Source7: activemq-wrapper.conf
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: tanukiwrapper >= 3.5.9

#%define buildver 5.1.0

%define homedir %{_prefix}/%{_name}
%define libdir %{homedir}/lib
%define datadir /var/cache/%{_name}
%define docsdir /usr/share/doc/%{name}-%{version}

%description
ApacheMQ is a JMS Compliant Messaging System

%prep
%setup -q -n apache-activemq-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
install --directory ${RPM_BUILD_ROOT}
install --directory ${RPM_BUILD_ROOT}%{homedir}
install --directory ${RPM_BUILD_ROOT}%{homedir}/bin
install --directory ${RPM_BUILD_ROOT}%{docsdir}
install --directory ${RPM_BUILD_ROOT}%{libdir}
install --directory ${RPM_BUILD_ROOT}%{homedir}/webapps
install --directory ${RPM_BUILD_ROOT}%{datadir}
install --directory ${RPM_BUILD_ROOT}%{datadir}/data
install --directory ${RPM_BUILD_ROOT}%{_localstatedir}/log/%{name}
install --directory ${RPM_BUILD_ROOT}%{_localstatedir}/run/%{name}
install --directory ${RPM_BUILD_ROOT}%{_sysconfdir}/%{_name}
install --directory ${RPM_BUILD_ROOT}%{_initrddir}

# Config files
install %{_sourcedir}/activemq.xml ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{_name}/activemq.xml
install %{_sourcedir}/activemq-wrapper.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{_name}/activemq-wrapper.conf
install %{_sourcedir}/activemq.credentials.properties ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{_name}/credentials.properties
install %{_sourcedir}/activemq.jetty.xml ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{_name}/jetty.xml
install %{_sourcedir}/activemq.log4j.properties ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{_name}/log4j.properties
install %{_sourcedir}/activemq.jetty-realm.properties ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{_name}/jetty-realm.properties

# startup script
#install bin/activemq ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
install %{_sourcedir}/activemq.init.rh ${RPM_BUILD_ROOT}%{_initrddir}/%{name}

# Bin and doc dirs
install *.txt *.html ${RPM_BUILD_ROOT}%{docsdir}
cp -r docs ${RPM_BUILD_ROOT}%{docsdir}

install bin/activemq.jar bin/activemq-admin ${RPM_BUILD_ROOT}%{homedir}/bin
#install --directory ${RPM_BUILD_ROOT}%{_bindir}
#%{__ln_s} -f %{homedir}/bin/activemq-admin ${RPM_BUILD_ROOT}%{_bindir}

# Runtime directory
cp -r lib/* ${RPM_BUILD_ROOT}%{libdir}
cp -r webapps/admin ${RPM_BUILD_ROOT}%{homedir}/webapps

pushd ${RPM_BUILD_ROOT}%{homedir}
    [ -d conf ] || %{__ln_s} -f %{_sysconfdir}/%{_name} conf
    [ -d data ] || %{__ln_s} -f %{datadir}/data data
    [ -d docs ] || %{__ln_s} -f %{docsdir} docs
    [ -d log ] || %{__ln_s} -f %{_localstatedir}/log/%{name} log 
popd


%pre
# Add the "activemq" user and group
/usr/sbin/groupadd -r %{name} 2> /dev/null || :

if getent passwd activemq > /dev/null ; then
  /usr/sbin/usermod -s /sbin/nologin activemq 2> /dev/null || :
else
  /usr/sbin/useradd -c "Apache Activemq" -g %{name} \
    -s /sbin/nologin -r -d %{homedir} %{name} 2> /dev/null || :
fi

%post
# install activemq (but don't activate)
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
    [ -f /var/lock/subsys/%{name} ] && %{_initrddir}/%{name} stop
    [ -f %{_initrddir}/%{name} ] && /sbin/chkconfig --del %{name}
fi

%postun

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
#%attr(755,root,root) %{_bindir}/activemq-admin
%{homedir}
%{homedir}/webapps
%docdir %{docsdir}
%{docsdir}
%{libdir}
%attr(775,activemq,activemq) %dir %{_localstatedir}/log/%{name}
%attr(775,activemq,activemq) %dir %{_localstatedir}/run/%{name}
%attr(755,activemq,activemq) %dir %{datadir}/data
%attr(755,root,root) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{_name}/activemq.xml
%config(noreplace) %{_sysconfdir}/%{_name}/activemq-wrapper.conf
%config(noreplace) %attr(750,root,activemq) %{_sysconfdir}/%{_name}/credentials.properties
%config(noreplace) %{_sysconfdir}/%{_name}/jetty.xml
%config(noreplace) %{_sysconfdir}/%{_name}/jetty-realm.properties
%config(noreplace) %{_sysconfdir}/%{_name}/log4j.properties

%changelog
* Fri May 10 2013 Robert Valk <robert.valk@sixtree.com.au> - 5.8.0-1
- Update activemq to version 5.8.0

* Thu Jun 28 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 5.6.0-2.pe
- Update activemq.jetty.xml to 5.6.0 for changed classnames

* Thu Jun 21 2012 Moses Mendoza <moses@puppetlabs.com> - 5.6.0-1.pe
- Update activemq to version 5.6.0

* Wed Mar 21 2012 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-7.pe
- Ensure admin interface is only listening on localhost

* Thu Oct 27 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-6.5.pe
- Update ActiveMQ configuration

* Thu Oct 27 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-6.4.pe
- Don't explicitly depend on java

* Thu Sep 15 2011 Matthaus Litteken <matthaus@puppetlabs.com> - 5.5.0-6.3.pe
- Init script fixed to recreate /var/run/activemq as needed.

* Thu Sep 15 2011 Matthaus Litteken <matthaus@puppetlabs.com> - 5.5.0-6.2.pe
- Init script fixed to give user a shell.

* Thu Sep 15 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-5.1.pe
- Init script typo fixed

* Wed Sep 07 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-5.pe
- Useradd no longer specifies a uid

* Fri Aug 19 2011 Matthaus Litteken <matthaus@puppetlabs.com> 5.5.0-4.pe
- Updated group and permissions on datadir. Bumped release to 4.

* Thu Aug 18 2011 Matthaus Litteken <matthaus@puppetlabs.com> 5.5.0-3
- Bumped release to 3 for PE 1.2.

* Thu May 12 2011 Ken Barber <ken@puppetlabs.com> 5.5.0-2
- Updated to 5.5.0. Adapted to PE.

* Sat Jan 16 2010 R.I.Pienaar <rip@devco.net> 5.3.0-1
- Adjusted for ActiveMQ 5.3.0 

* Wed Oct 29 2008 James Casey <james.casey@cern.ch> 5.2.0-2
- fixed defattr on subpackages 

* Tue Sep 02 2008 James Casey <james.casey@cern.ch> 5.2.0-1
- Upgraded to activemq 5.2.0

* Tue Sep 02 2008 James Casey <james.casey@cern.ch> 5.1.0-7
- Added separate logging of messages whenever the logging interceptor is enabled in the config file
- removed BrokerRegistry messages casued by REST API
- now we don't log messages to stdout (so no duplicates in wrapper log).
- upped the number and size of the rolling logs

* Fri Aug 29 2008 James Casey <james.casey@cern.ch> 5.1.0-6
- make ServiceData be correct LDIF

* Wed Aug 27 2008 James Casey <james.casey@cern.ch> 5.1.0-5
- changed glue path from mds-vo-name=local to =resource

* Tue Aug 05 2008 James Casey <james.casey@cern.ch> 5.1.0-4
- fixed up info-provider to give both REST and STOMP endpoints

* Mon Aug 04 2008 James Casey <james.casey@cern.ch> 5.1.0-3
- reverted out APP_NAME change to ActiveMQ from init.d since it 
  causes too many problems
* Mon Aug 04 2008 James Casey <james.casey@cern.ch> 5.1.0-2
- Added info-provider
- removed mysql as a requirement

* Thu Mar 20 2008 Daniel RODRIGUES <daniel.rodrigues@cern.ch> - 5.1-SNAPSHOT-1
- Changed to version 5.1 SNAPSHOT of 18 Mar, fizing AMQ Message Store 
- small fixes to makefile

* Fri Dec 14 2007 James CASEY <james.casey@cern.ch> - 5.0.0-3rc4
- Added apache config file to forward requests to Jetty

* Thu Dec 13 2007 James CASEY <james.casey@cern.ch> - 5.0.0-2rc4
- fixed /usr/bin symlink
- added useJmx to the default config

* Thu Dec 13 2007 James CASEY <james.casey@cern.ch> - 5.0.0-RC4.1
- Moved to RC4 of the 5.0.0 release candidates

* Mon Dec 10 2007 James CASEY <james.casey@cern.ch> - 5.0-SNAPSHOT-7
- added symlink in /usr/bin for activemq-admin

* Wed Nov 26 2007 James CASEY <james.casey@cern.ch> - 5.0-SNAPSHOT-6
- fix bug with group name setting in init.d script

* Wed Nov 26 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-5
- fix typos in config file for activemq

* Wed Nov 26 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-4
- add support for lib64 version of tanukiwrapper in config
- turned off mysql persistence in the "default" config

* Wed Oct 17 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-2
- more re-org to mirror how tomcat is installed.
- support for running as activemq user

* Tue Oct 16 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-1
- Initial Version

