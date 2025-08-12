%global cachedir %{_localstatedir}/cache/ddclient
%global rundir   %{_rundir}/ddclient

Summary:           Client to update dynamic DNS host entries
Name:              ddclient
Version:           4.0.0
Release:           1%{?dist}
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:           GPL-2.0-or-later
URL:               https://ddclient.net/
Source0:           https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:           ddclient.rwtab
Source2:           ddclient.service
Source3:           ddclient.sysconfig
Source4:           ddclient.NetworkManager
Source5:           ddclient-tmpfiles.conf

BuildArch:         noarch

BuildRequires:     autoconf
BuildRequires:     automake
BuildRequires:     make
BuildRequires:     perl-generators
BuildRequires:     perl(Sys::Hostname)
BuildRequires:     perl(version)
BuildRequires:     systemd-rpm-macros
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

# For tests
BuildRequires:     iproute
BuildRequires:     perl(HTTP::Daemon)
BuildRequires:     perl(HTTP::Daemon::SSL)
BuildRequires:     perl(HTTP::Message::PSGI)
BuildRequires:     perl(HTTP::Request)
BuildRequires:     perl(HTTP::Response)
BuildRequires:     perl(IO::Socket::INET6)
BuildRequires:     perl(Test::MockModule)
BuildRequires:     perl(Test::TCP)
BuildRequires:     perl(Test::Warnings)
BuildRequires:     perl(Time::HiRes)

Requires:          perl(Data::Validate::IP)
Requires:          perl(Digest::SHA1)
Requires:          perl(IO::Socket::INET6)
Requires:          perl(IO::Socket::SSL)
Requires:          perl(JSON::PP)

# Old NetworkManager expects the dispatcher scripts in a different place
Conflicts:         NetworkManager < 1.20

%description
ddclient is a Perl client used to update dynamic DNS entries for accounts
on many different dynamic DNS services. Features include: Operating as a
daemon, manual and automatic updates, static and dynamic updates, optimized
updates for multiple addresses, MX, wildcards, abuse avoidance, retrying
the failed updates and sending update status to syslog and through e-mail.

%prep
%autosetup -p 1
# Send less mail by default, eg. not on every shutdown.
sed -e 's|^mail=|#mail=|' -i ddclient.conf.in
./autogen

# Create a sysusers.d config file
cat >ddclient.sysusers.conf <<EOF
u ddclient - 'Dynamic DNS Client' %{cachedir} -
EOF


%build
%configure --runstatedir=%{rundir} --with-confdir='%{sysconfdir}'
make %{?_smp_mflags}

%install
install -D -p -m 755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 600 ddclient.conf %{buildroot}%{_sysconfdir}/%{name}.conf

install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rwtab.d/%{name}
install -D -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -p -m 755 %{SOURCE4} %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/50-%{name}
install -D -p -m 644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}%{cachedir}
mkdir -p %{buildroot}%{rundir}
touch %{buildroot}%{cachedir}/%{name}.cache

# Correct permissions for later usage in %doc
chmod 644 sample-*

install -m0644 -D ddclient.sysusers.conf %{buildroot}%{_sysusersdir}/ddclient.conf


%check
make VERBOSE=1 check



%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license COPYING COPYRIGHT
%doc README* ChangeLog.md sample-etc_ppp_ip-up.local
%doc sample-etc_dhclient-exit-hooks sample-etc_cron.d_ddclient
%doc sample-ddclient-wrapper.sh sample-etc_dhcpc_dhcpcd-eth0.exe

%{_sbindir}/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service

# sysconfdir
%config(noreplace) %{_sysconfdir}/rwtab.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(600,ddclient,ddclient) %config(noreplace) %{_sysconfdir}/%{name}.conf
%{_prefix}/lib/NetworkManager/dispatcher.d/50-%{name}

# localstatedir
%attr(0700,ddclient,ddclient) %dir %{cachedir}
%attr(0600,ddclient,ddclient) %ghost %{cachedir}/%{name}.cache
%ghost %attr(0755,ddclient,ddclient) %dir %{rundir}
%{_sysusersdir}/ddclient.conf


%changelog
* Sun Aug 10 2025 Your Name <your@email.com> - 4.0.0-1.el10
- Initial build for EPEL 10 from Fedora 42 sources (version 4.0.0).
- Switched to sysusers.d for user creation.
- Updated build process for autoconf/automake.

