Summary:	Traffic Flow Analysis Tool
Name:		cflowd
Version:	2.1.b1
Release:	1
Epoch:		0
License:	GPL
Obsoletes:      cflowd0-devel
Group:		Applications/Networking
Source0:	ftp://ftp.caida.org/pub/cflowd/%{name}-2-1-b1.tar.gz
# Source0-md5:	6f0543390e9d46c4274f6b12b6517f62
Source1:	%{name}.init
Patch0:		%{name}-yywrap.patch
# http://net.doit.wisc.edu/~plonka/cflowd/cflowd-2-1-b1-djp.patch
Patch1:		http://net.doit.wisc.edu/~plonka/cflowd/cflowd-djp.patch
BuildRequires:	arts++-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	perl-base
URL:		http://www.caida.org/tools/measurement/cflowd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
cflowd is a flow analysis tool currently used for analyzing Cisco's
NetFlow enabled switching method. The current release (described
below) includes the collections, storage, and basic analysis modules
for cflowd and for arts++ libraries. This analysis package permits
data collection and analysis by ISPs and network engineers in support
of capacity planning, trends analysis, and characterization of
workloads in a network service provider environment. Other areas where
cflowd may prove useful include usage tracking for Web hosting,
accounting and billing, network planning and analysis, network
monitoring, developing user profiles, data warehousing and mining, as
well as security-related investigations.

%package libs
Summary:        cflowd libraries
Group:          Libraries

%description libs
cflowd libraries.

%package devel
Summary:        Header files and develpment documentation for cflowd
Group:          Development/Libraries
Requires:       %{name}-libs = %{epoch}:%{version}

%description devel
Header files and develpment documentation for cflowd.

%package static
Summary:        Static cflowd libraries
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}

%description static
Static cflowd libraries.

%prep
%setup -q -n %{name}-2-1-b1
%patch0 -p1
%patch1 -p0

%build
chmod u+w *.m4 configure
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--enable-shared

perl -pi -e 's#libtool#libtool --tag=CXX#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile*
perl -pi -e 's#/usr/local/arts/include/#%{_includedir}/arts++/#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile*

%{__make} \
	ARTSPPINC="-I%{_includedir}/arts++" \
	ARTSCLASSINC="-I%{_includedir}/arts++" \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/lib/cflowd}

perl -pi -e 's#/usr/include#\$\(includedir\)/%{name}#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile* */*/*/*/Makefile*
perl -pi -e 's#\$\(includedir\)/%{name}/arts\+\+#/usr/include/arts\+\+#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile* */*/*/*/Makefile*
perl -pi -e 's#/usr/lib#\$\(libdir\)#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile* */*/*/*/Makefile*
perl -pi -e 's#/usr/bin#\$\(bindir\)#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile* */*/*/*/Makefile*
perl -pi -e 's#/usr/sbin#\$\(sbindir\)#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile* */*/*/*/Makefile*
perl -pi -e 's#/usr/share/man#\$\(mandir\)#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile* */*/*/*/Makefile*
perl -pi -e 's#/etc/%{name}#\$\(sysconfdir\)#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile* */*/*/*/Makefile*

%{makeinstall}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

cp -f $RPM_BUILD_ROOT%{_sysconfdir}/cfdcollect.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/cfdcollect.conf
cp -f $RPM_BUILD_ROOT%{_sysconfdir}/cflowd.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/cflowd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
        /etc/rc.d/init.d/%{name} restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} service."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/%{name} ]; then
                /etc/rc.d/init.d/%{name} stop 1>&2
        fi
        /sbin/chkconfig --del %{name}
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README doc/configuration/{*.html,*.gif}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(750,root,root) /var/lib/%{name}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
