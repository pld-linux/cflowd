Summary:	command line utilities analyzing sFlow data
Name:		cflowd
Version:	2.1
Release:	0.b1.1
License:	GPL
Group:		Applications/Networking
Source0:	ftp://ftp.caida.org/pub/cflowd/cflowd-2-1-b1.tar.gz
# Source0-md5:
BuildRequires:	arts++-devel
URL:		http://www.caida.org/tools/measurement/cflowd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cflowd is a flow analysis tool currently used for analyzing Cisco's NetFlow enabled switching method. The current release (described below) includes the collections, storage, and basic analysis modules for cflowd and for arts++ libraries. This analysis package permits data collection and analysis by ISPs and network engineers in support of capacity planning, trends analysis, and characterization of workloads in a network service provider environment. Other areas where cflowd may prove useful include usage tracking for Web hosting, accounting and billing, network planning and analysis, network monitoring, developing user profiles, data warehousing and mining, as well as security-related investigations.

%prep
%setup -q -n %{name}-2-1-b1

%build
install %{_datadir}/automake/config.* .
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
