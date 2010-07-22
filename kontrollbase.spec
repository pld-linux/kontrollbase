# TODO
# - system extjs package
%define		subver	rev312
%define		rel		0.1
Summary:	Enterprise grade MySQL monitoring and analytics
Name:		kontrollbase
Version:	2.0.1
Release:	0.%{subver}.%{rel}
License:	New BSD License
Group:		Applications/WWW
Source0:	http://kontrollbase.googlecode.com/files/%{name}-%{subver}.tar.gz
# Source0-md5:	de68aac4e8ec18c0adea8a76f0e455a3
URL:		http://code.google.com/p/kontrollbase/
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
An Enterprise Class MySQL Monitoring and Analytics Application
- A monitoring system that is specificly designed for MySQL servers
  from the ground up. We aren't wasting time trying to be everything for
  everyone - there are no checks for Cisco or OSX or Windows here.
- Features in depth analysis and performance tuning recommendations
  for your servers.
- A large range of performance graphs for historical data analysis and
  data correlation.
- A large range of alerts so you are always kept up to date on your
  server's health.
- A monitoring system that is secure and has code that is available
  for anyone to audit.
- An API so that you can read data and alerts remotely for integration
  with ticketing systems and enterprise analytics tools.
- An application that will run on the LAMP stack, use minimal
  resources, and is intuitive to use.
- A multi-tier authentication so that DBAs, managers, system
  engineers, and hosting or SaaS clients can login and see how their
  databases are responding.
- You do not want to be forced into a service contract or software
  license agreement that costs hundreds or thousands of dollars per
  server per year.
- A consistent release cycle that listens to user input and feature
  requests.
- A human support system - not the typical corporate run-around or
  off-shore nonsense.
- If you want all of those features then Kontrollbase is the answer
  for you.

%prep
%setup -q -n %{name}-%{subver}
%undos -f js,php

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a . $RPM_BUILD_ROOT%{_appdir}

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
#%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
