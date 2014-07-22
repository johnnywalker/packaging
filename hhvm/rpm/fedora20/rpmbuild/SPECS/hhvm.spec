# add --with debug to build additional debug package
%bcond_with debug

# disable debuginfo package and just use separate debug build if requested
# debuginfo generation seems to break hhvm's embedded php
%global debug_package %{nil}

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
BuildRequires: php55u-cli
BuildRequires: php55u-posix
BuildRequires: php55u-process
BuildRequires: php55u-pecl-jsonc
%endif

%if (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
BuildRequires: php-cli
BuildRequires: php-posix
BuildRequires: php-process
BuildRequires: php-pecl-jsonc
BuildRequires: libzip-devel
%endif

# end of distribution specific definitions

# source on GitHub
%global commit 48f9820dcd24f61d0c43d85be8d1945041cfa816
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global repoowner facebook
%global reponame hhvm
%global stdname hhvm
%global sm0_destpath third-party
%global sm0_commit 1b7752522776202e7051031004cd12d97302872f
%global sm0_shortcommit %(c=%{commit}; echo ${c:0:7})
%global sm0_repoowner hhvm
%global sm0_reponame hhvm-third-party
%global sm1_destpath third-party/folly/src
%global sm1_commit 09a81a96ea2f9790242675f3c84013266c38d684
%global sm1_shortcommit %(c=%{commit}; echo ${c:0:7})
%global sm1_repoowner facebook
%global sm1_reponame folly

Name:           hhvm
Summary:        HHVM is a new open-source virtual machine designed for executing programs written in PHP. HHVM uses a just-in-time (JIT) compilation approach to achieve superior performance while maintaining the flexibility that PHP developers are accustomed to.  http://hhvm.com
Version:        3.2
Release:        11.20140718git%{shortcommit}%{?dist}
License:        PHP and Zend
Group:          Development/Compilers
Provides:       hiphop-php
Url:            https://github.com/facebook/hhvm
Source0:        https://github.com/%{repoowner}/%{reponame}/archive/%{commit}/%{reponame}-%{commit}.tar.gz
Source1:        https://github.com/%{sm0_repoowner}/%{sm0_reponame}/archive/%{sm0_commit}/%{sm0_reponame}-%{sm0_commit}.tar.gz
Source2:        https://github.com/%{sm1_repoowner}/%{sm1_reponame}/archive/%{sm1_commit}/%{sm1_reponame}-%{sm1_commit}.tar.gz
Source3:        php.ini
Source4:        server.hdf
Source5:        config.hdf
Source6:        static.mime-types.hdf
Source7:        hhvm.init
Source8:        hhvm.sysconf
Source9:        hhvm.logrotate
Source10:       hhvm.service
Source11:       curl.license
Source12:       libafdt.license
Source13:       libglog.license
Source14:       libmbfl.license
Source15:       lz4.license
Source16:       PHP.license
Source17:       sqlite3.license
Source18:       THIRD_PARTY.license
Source19:       timelib.license
Source20:       ZEND.license
Patch:          0001-Use-GNUInstallDirs.cmake.patch
Patch1:         0002-use-CMAKE_INSTALL_-DIR-indirection-in-HHVM_INSTALL-f.patch
Patch2:         0003-adjustments-for-GNUInstallDirs.patch
Patch3:         0004-use-third-party-sqlite3-if-pkg-config-reports-versio.patch
Patch4:         0005-specify-ssl-cipher-list-for-curl-with-OpenSSL-only.patch
Patch5:         0007-point-third-party-submodule-at-fork.patch
Patch6:         third-party_0001-use-GNUInstallDirs.patch
Patch7:         third-party_0002-disable-libzip-install.patch
BuildRoot:      %{_tmppath}/build-root-%{name}-%{version}
BuildArch:      x86_64
BuildRequires: bison
BuildRequires: binutils
BuildRequires: cmake >= 2.8.7
BuildRequires: flex
BuildRequires: gcc >= 4.7.2
BuildRequires: git
BuildRequires: perl
BuildRequires: binutils-devel
BuildRequires: boost-devel >= 1.50
BuildRequires: bzip2-devel
BuildRequires: curl-devel >= 7.29.0
BuildRequires: elfutils-libelf-devel
BuildRequires: expat-devel
BuildRequires: jemalloc-devel >= 3.4
BuildRequires: gd-devel
BuildRequires: glog-devel >= 0.3.3
BuildRequires: ImageMagick-devel
BuildRequires: inotify-tools-devel
BuildRequires: libcap-devel
BuildRequires: libc-client-devel
BuildRequires: libdwarf-devel
BuildRequires: libedit-devel
BuildRequires: libevent-devel >= 1.4.14
BuildRequires: libicu >= 4.8
BuildRequires: libIDL-devel
BuildRequires: libmcrypt-devel >= 2.5.8
BuildRequires: libmemcached-devel >= 1.0.9
BuildRequires: libyaml-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: mysql-devel
BuildRequires: oniguruma-devel
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: pcre-devel
BuildRequires: readline-devel
BuildRequires: snappy-devel >= 1.1.0
BuildRequires: tbb-devel >= 4
BuildRequires: zlib-devel
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
%if %{use_systemd}
    %{?systemd_requires: %systemd_requires}
%endif

%description
HipHop for PHP is an open source project developed by Facebook. HipHop offers a PHP execution engine called the "HipHop Virtual Machine" (HHVM) which uses a just-in-time compilation approach to achieve superior performance. To date, Facebook has achieved more than a 6x reduction in CPU utilization for the site using HipHop as compared with Zend PHP.

%if %{with debug}
%package debug
Summary: debug version of HHVM
Group: System Environment/Daemons
Requires: hhvm
%description debug
Not stripped version of HHVM with -DCMAKE_BUILD_TYPE=Debug
%endif

%prep
%setup -q -T -c
%setup -q -T -D -b 0
%{__mv} -T ../%{reponame}-%{commit} $PWD
%setup -q -T -D -b 1
%{__mv} -T ../%{sm0_reponame}-%{sm0_commit} %{sm0_destpath}
%setup -T -D -b 2
%{__mv} -T ../%{sm1_reponame}-%{sm1_commit} %{sm1_destpath}
%patch -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
cd third-party
%patch6 -p1
%patch7 -p1

%build
export CMAKE_PREFIX_PATH=%{_prefix}
%if %{with debug}
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_BUILD_TYPE=Debug
%{__make} %{?_smp_mflags}
%{__mv} %{_builddir}/%{name}-%{version}/hphp/hhvm/hhvm \
        %{_builddir}/%{name}-%{version}/hphp/hhvm/hhvm.debug
%endif
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_BUILD_TYPE=Release
%{__make} %{?_smp_mflags}

%check
export TRAVIS=spoof     # fool test script into thinking we're CI
./hphp/test/run

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# Install Config files in /etc/hhvm
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/hhvm
%{__install} -m 644 -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/hhvm
%{__install} -m 644 -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/hhvm
files_with_macros="$files_with_macros $RPM_BUILD_ROOT%{_sysconfdir}/hhvm/%{basename:%{SOURCE4}}"
%{__install} -m 644 -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/hhvm

# Setup Static types
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/hhvm/hdf
%{__install} -m 644 -p %{SOURCE6} \
    $RPM_BUILD_ROOT%{_datadir}/hhvm/hdf/static.mime-types.hdf

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
%{__install} -m 644 -p %{SOURCE8} \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/hhvm
files_with_macros="$files_with_macros $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/hhvm"

%if %{use_systemd}
# Setup service script for systemd
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE10 \
        $RPM_BUILD_ROOT%{_unitdir}/hhvm.service
files_with_macros="$files_with_macros $RPM_BUILD_ROOT%{_unitdir}/hhvm.service"
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_initrddir}/hhvm
files_with_macros="$files_with_macros $RPM_BUILD_ROOT%{_initrddir}/hhvm"
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE9} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/hhvm
files_with_macros="$files_with_macros $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/hhvm"

%if %{with debug}
%{__install} -m644 %{_builddir}/%{name}-%{version}/hphp/hhvm/hhvm.debug \
   $RPM_BUILD_ROOT%{_bindir}/hhvm.debug
%endif

# create /var directories
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/cache/hhvm
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/log/hhvm
%{__mkdir} -p $RPM_BUILD_ROOT%{_localstatedir}/run/hhvm

# Setup Licenses
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE

%{__cp} %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE11} .license)
%{__cp} %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE12} .license)
%{__cp} %{SOURCE13} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE13} .license)
%{__cp} %{SOURCE14} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE14} .license)
%{__cp} %{SOURCE15} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE15} .license)
%{__cp} %{SOURCE16} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE16} .license)
%{__cp} %{SOURCE17} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE17} .license)
%{__cp} %{SOURCE18} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE18} .license)
%{__cp} %{SOURCE19} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE19} .license)
%{__cp} %{SOURCE20} $RPM_BUILD_ROOT%{_datadir}/hhvm/LICENSE/$(basename %{SOURCE20} .license)

# process macros
%{__sed} -i -e s#@_bindir@#%{_bindir}#g $files_with_macros
%{__sed} -i -e s#@_datadir@#%{_datadir}#g $files_with_macros
%{__sed} -i -e s#@_localstatedir@#%{_localstatedir}#g $files_with_macros
%{__sed} -i -e s#@_sysconfdir@#%{_sysconfdir}#g $files_with_macros

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)

%config(noreplace) %{_sysconfdir}/hhvm/config.hdf
%config(noreplace) %{_sysconfdir}/hhvm/server.hdf
%config(noreplace) %{_sysconfdir}/hhvm/php.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/hhvm
%config(noreplace) %{_sysconfdir}/sysconfig/hhvm
%if %{use_systemd}
%{_unitdir}/hhvm.service
%else
%{_initrddir}/hhvm
%endif

%attr(775, www-data, www-data) %{_localstatedir}/cache/hhvm/
%attr(775, www-data, www-data) %{_localstatedir}/run/hhvm/
%attr(775, www-data, www-data) %{_localstatedir}/log/hhvm/

%{_bindir}/hhvm
%{_bindir}/hphpize
%ghost %attr(755,root,root) %{_bindir}/php
%{_includedir}/*
%{_libdir}/*
%{_datadir}/*

%if %{with debug}
%files debug
%attr(0755,root,root) %{_bindir}/hhvm.debug
%endif

%pre
# 
# hhvm package first install:
#
if [ $1 -eq 1 ]; then
    /usr/sbin/useradd -c "www-data" -d /var/www -s /sbin/nologin -r www-data 2>/dev/null || :
fi

%post
/sbin/ldconfig
%{_sbindir}/update-alternatives --install %{_bindir}/php php %{_bindir}/hhvm 60
%if %{use_systemd}
    %systemd_post %{name}.service
%else
# 
# package first install:
#
    if [ $1 -eq 1 ]; then
        /sbin/chkconfig --add %{name} &> /dev/null || :
    fi
%endif

%preun
%if %{use_systemd}
    %systemd_preun %{name}.service
%else
#
# package removal:
#
# Stop a running 'hhvm' service and remove start/stop links...
    if [ $1 -eq 0 ]; then
            /sbin/service %{name} stop > /dev/null 2>&1 || :
            /sbin/chkconfig --del %{name} &> /dev/null || :
    fi
%endif

%postun
/sbin/ldconfig
#
# Package removal:
#
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove php %{_bindir}/hhvm
fi
%if %{use_systemd}
    %systemd_postun_with_restart %{name}.service
%else
#
# package upgrade:
#
# If 'hhvm' was running, stop it and restart it with the upgraded version...
    if [ $1 -ge 1 ]; then
        /sbin/service %{name} condrestart >/dev/null 2>&1 || :
    fi
%endif

%changelog
* Wed Jul 23 2014 Johnny Walker <jwalker (at) ashley-martin.com>
- default values for init script and systemd service variables
- updated misc files to use macros for various dirs
- default HHVM central repo to /var/cache/hhvm (in server.hdf)
- remove incorrect Type=forking from systemd service def

* Tue Jul 22 2014 Johnny Walker <jwalker (at) ashley-martin.com>
- working 3.2 release
- conditional debug build (--with debug generates an additional hhvm-debug package)
- licenses included and installed in %{_datadir}/hhvm/LICENSE
- patches included to use GNU install dirs (e.g. /usr/lib64)
- git source snapshots removed from repo
- SSL cipher list patch included
- sqlite3 build patch included (ignore installed sqlite3 == 3.8.5)
- compatible with sysvinit and systemd
- compatible with RHEL/CentOS and Fedora
- updated rpm metadata (license, url)
- added %post, %preun, and %postun actions for systemd and sysvinit
- removed libzip install files (conflicts with actual libzip)
- use automatic dependency resolution
- updated SysV init script to follow standards better and support condrestart
