# $Id$
# Authority: dag
# Upstream: <cacti-user$lists,sf,net>

%{?rh7:%define _without_net_snmp 1}
%{?el2:%define _without_net_snmp 1}
%{?rh6:%define _without_net_snmp 1}

Summary: Fast c-based poller for the cacti graphing solution
Name: cacti-spine
Version: 0.8.8b
Release: 1%{dist}
License: LGPLv2+
Group: Applications/System
URL: http://www.cacti.net/

Packager: Marco Tizzoni <marco.tizzoni@gmail.com>

Source: http://www.cacti.net/downloads/spine/cacti-spine-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: mysql-devel, openssl-devel, automake, libtool

%{!?_without_net_snmp:BuildRequires: net-snmp-devel, net-snmp-utils}
%{?_without_net_snmp:BuildRequires: ucd-snmp-devel, ucd-snmp-utils}

Requires: cacti => 0.8.7

%description
Spine is a supplemental poller for Cacti that makes use of pthreads
to achieve excellent performance.

%prep
%setup

### FIXME: Patch to use /usr/lib64 on 64bit (Please fix upstream)
%{__perl} -pi.orig -e 's|/lib\b|/%{_lib}|g' configure

%build
autoreconf --force --install --symlink
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m0755 spine %{buildroot}%{_bindir}/spine
%{__install} -Dp -m0644 spine.conf.dist %{buildroot}%{_sysconfdir}/spine.conf

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING LICENSE* README
%{_bindir}/spine

%defattr(-, cacti, cacti, 0755)
%config(noreplace) %{_sysconfdir}/spine.conf

%changelog
* Wed May 07 2014 Marco Tizzoni <marco.tizzoni@gmail.com> - 0.8.8b-1
- New version
- Set spine suid for use with boost
