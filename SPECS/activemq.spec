Summary: Apache ActiveMQ
Name: activemq
Version: 5.8.0
Release: 3%{?dist}
License: ASL 2.0
Group: System Environment/Daemons
URL: http://activemq.apache.org/
Source0: http://www.apache.org/dist//activemq/apache-activemq/%{version}/apache-activemq-%{version}-bin.tar.gz
Source1: wlcg-patch.tgz
Source2: activemq.xml
Source3: jetty-realm.properties
Source4: jetty.xml
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: tanukiwrapper >= 3.2.0

%define homedir /usr/share/%{name}
%define libdir /var/lib/%{name}
%define libexecdir /usr/libexec/%{name}
%define cachedir /var/cache/%{name}
%define docsdir /usr/share/doc/%{name}-%{version}

%description
ApacheMQ is a JMS Compliant Messaging System

%package info-provider
Summary: An LDAP information provider for activemq
Group:grid/lcg
%description info-provider
An LDAP infomation provider for activemq

%package meta
Summary: A metapackage
Group:grid/lcg
Requires: activemq = %{version}-%{release}, activemq-info-provider = %{version}-%{release}
%description meta
A metapackage

%prep
%setup -q -a1 -n apache-activemq-%{version}

%build
install --directory ${RPM_BUILD_ROOT}

%install
rm -rf $RPM_BUILD_ROOT
install --directory ${RPM_BUILD_ROOT}%{homedir}
install --directory ${RPM_BUILD_ROOT}%{homedir}/bin
install --directory ${RPM_BUILD_ROOT}%{docsdir}
install --directory ${RPM_BUILD_ROOT}%{libdir}/lib
install --directory ${RPM_BUILD_ROOT}%{libexecdir}
install --directory ${RPM_BUILD_ROOT}%{libdir}/webapps
install --directory ${RPM_BUILD_ROOT}%{cachedir}
install --directory ${RPM_BUILD_ROOT}%{cachedir}/data
install --directory ${RPM_BUILD_ROOT}/var/log/%{name}
install --directory ${RPM_BUILD_ROOT}/var/run/%{name}
install --directory ${RPM_BUILD_ROOT}/etc/%{name}
install --directory ${RPM_BUILD_ROOT}%{_initrddir}
install --directory ${RPM_BUILD_ROOT}/etc/httpd/conf.d

# Config files
install %{SOURCE2} ${RPM_BUILD_ROOT}/etc/%{name}
install conf/credentials.properties ${RPM_BUILD_ROOT}/etc/%{name}
install conf/jetty.xml  ${RPM_BUILD_ROOT}/etc/%{name}
install %{SOURCE3} ${RPM_BUILD_ROOT}/etc/%{name}
install %{SOURCE4} ${RPM_BUILD_ROOT}/etc/%{name}
install conf/log4j.properties ${RPM_BUILD_ROOT}/etc/%{name}
install conf/activemq-wrapper.conf ${RPM_BUILD_ROOT}/etc/%{name}
install conf/activemq-httpd.conf ${RPM_BUILD_ROOT}/etc/httpd/conf.d

# startup script
install bin/activemq ${RPM_BUILD_ROOT}%{_initrddir}

# Bin and doc dirs
install *.txt *.html LICENSE NOTICE ${RPM_BUILD_ROOT}%{docsdir}
cp -r docs ${RPM_BUILD_ROOT}%{docsdir}

install bin/activemq.jar bin/activemq-admin ${RPM_BUILD_ROOT}%{homedir}/bin
install --directory ${RPM_BUILD_ROOT}/usr/bin
%{__ln_s} -f %{homedir}/bin/activemq-admin ${RPM_BUILD_ROOT}/usr/bin

# Runtime directory
cp -r lib ${RPM_BUILD_ROOT}%{libdir}
cp -r webapps/admin ${RPM_BUILD_ROOT}%{libdir}/webapps

# Info provider
install info-provider-activemq ${RPM_BUILD_ROOT}/%{libexecdir}

pushd ${RPM_BUILD_ROOT}%{homedir}
    [ -d conf ] || %{__ln_s} -f /etc/%{name} conf
    [ -d data ] || %{__ln_s} -f %{cachedir}/data data
    [ -d docs ] || %{__ln_s} -f %{docsdir} docs
    [ -d lib ] || %{__ln_s} -f %{libdir}/lib lib
    [ -d log ] || %{__ln_s} -f /var/log/%{name} log
    [ -d webapps ] || %{__ln_s} -f %{libdir}/webapps webapps
popd

%pre
# Add the "activemq" user and group
# we need a shell to be able to use su - later
/usr/sbin/groupadd -g 92 -r activemq 2> /dev/null || :
/usr/sbin/useradd -c "Apache Activemq" -u 92 -g activemq \
    -s /bin/bash -r -d /usr/share/activemq activemq 2> /dev/null || :

# backup and move original config files
if [ -e /etc/%{name}/activemq.xml ]; then
   mv -f /etc/%{name}/activemq.xml /etc/%{name}/activemq.xml.orig
fi
if [ -e /etc/httpd/conf.d/activemq-wrapper.conf ]; then
   mv -f /etc/httpd/conf.d/activemq-wrapper.conf /etc/httpd/conf.d/activemq-wrapper.conf.orig
fi
if [ -e /etc/%{name}/log4j.properties ]; then
   mv -f /etc/%{name}/log4j.properties /etc/%{name}/log4j.properties.orig
fi
if [ -e /etc/%{name}/credentials.properties ]; then
   mv -f /etc/%{name}/credentials.properties /etc/%{name}/credentials.properties.orig
fi
if [ -e /etc/%{name}/jetty.xml ]; then
   mv -f /etc/%{name}/jetty.xml /etc/%{name}/jetty.xml.orig
fi
if [ -e /etc/%{name}/jetty-realm.properties ]; then
   mv -f /etc/%{name}/jetty-realm.properties /etc/%{name}/jetty-realm.properties.orig
fi

%post
# install activemq (but don't activate)
/sbin/chkconfig --add activemq

%preun
if [ $1 = 0 ]; then
    [ -f /var/lock/subsys/activemq ] && %{_initrddir}/activemq stop
    [ -f %{_initrddir}/activemq ] && /sbin/chkconfig --del activemq
fi

%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{homedir}
%docdir %{docsdir}
%{docsdir}
%{libdir}
%defattr(644,root,root)
%{libdir}/webapps/admin/WEB-INF/web.xml
%config(noreplace) /etc/httpd/conf.d/activemq-httpd.conf
%config(noreplace) /etc/%{name}/*
%attr(755,root,root) /usr/bin/activemq-admin
%attr(755,activemq,activemq) %dir /var/log/%{name}
%attr(755,activemq,activemq) %dir /var/run/%{name}
%attr(775,root,activemq) %dir %{cachedir}/data
%attr(755,root,root) %{_initrddir}/activemq

%files info-provider
%defattr(-,root,root)
%attr(755,root,root) %{libexecdir}/info-provider-activemq

%changelog
* Thu Oct 17 2013 Melissa Stone <melissa@puppetlabs.com> - 5.8.0-3
* It turns out rpmlint is a valuable tool to use

* Wed Oct 16 2013 Melissa Stone <melissa@puppetlabs.com> - 5.8.0-2
* Conf file fixes that were initially missed

* Tue Oct 15 2013 Melissa Stone <melissa@puppetlabs.com> - 5.8.0-1
* Update for 5.8.0

* Fri Sep 02 2011 Michael Stahnke <stahnma@fedoraproject.org> - 5.5.0-1
- Update for 5.5.0

* Sat Jan 16 2010 R.I.Pienaar <rip@devco.net> 5.3.0
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
