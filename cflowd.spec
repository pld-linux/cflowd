Summary:	Traffic Flow Analysis Tool
Summary(pl.UTF-8):	Narzędzie do analizy przepływu ruchu w sieci
Name:		cflowd
Version:	2.1.b1
Release:	1
Epoch:		0
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.caida.org/pub/cflowd/%{name}-2-1-b1.tar.gz
# Source0-md5:	6f0543390e9d46c4274f6b12b6517f62
Source1:	%{name}.init
Patch0:		%{name}-yywrap.patch
# http://net.doit.wisc.edu/~plonka/cflowd/cflowd-2-1-b1-djp.patch
Patch1:		http://net.doit.wisc.edu/~plonka/cflowd/%{name}-djp.patch
Patch2:		%{name}-gcc3.patch
Patch3:		%{name}-link.patch
Patch4:		%{name}-printf.patch
URL:		http://www.caida.org/tools/measurement/cflowd/
BuildRequires:	arts++-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool >= 2:1.4d-3
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	rc-scripts
Obsoletes:	cflowd0-devel
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

%description -l pl.UTF-8
cflowd to narzędzie do analizy przepływu ruchu w sieci aktualnie
używane dla switchy Cisco z włączonym mechanizmem NetFlow. Aktualne
wydanie (opisane poniżej) zawiera kolekcje, przechowywanie danych oraz
podstawowe moduły do analizy dla bibliotek cflowd i arts++. Ten pakiet
do analizy pozwala na zbieranie danych i analizę przez ISP oraz
inżynierów sieciowych wspierających planowanie możliwości sieci,
analizę trendów oraz charakterystykę obciążeń w środowisku providera
usług sieciowych. Inne obszary, gdzie cflowd może się okazać
przydatny, obejmują śledzenie hostowania WWW, naliczanie rachunków,
planowanie i analizę sieci, monitorowanie sieci, tworzenie profili
użytkowników, magazynowanie danych, a także badania związane z
bezpieczeństwem.

%package libs
Summary:	cflowd libraries
Summary(pl.UTF-8):	Biblioteki cflowd
Group:		Libraries

%description libs
cflowd libraries.

%description libs -l pl.UTF-8
Biblioteki cflowd.

%package devel
Summary:	Header files and development documentation for cflowd
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty dla cflowd
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for cflowd.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty dla cflowd.

%package static
Summary:	Static cflowd libraries
Summary(pl.UTF-8):	Statyczne biblioteki cflowd
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description static
Static cflowd libraries.

%description static -l pl.UTF-8
Statyczne biblioteki cflowd.

%prep
%setup -q -n %{name}-2-1-b1
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
chmod u+w *.m4 configure
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--enable-shared

sed -i -e 's#libtool#libtool --tag=CXX#g' Makefile* */Makefile* */*/Makefile* */*/*/Makefile*

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

%makeinstall

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

cp -f $RPM_BUILD_ROOT%{_sysconfdir}/cfdcollect.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/cfdcollect.conf
cp -f $RPM_BUILD_ROOT%{_sysconfdir}/cflowd.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/cflowd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

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
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
