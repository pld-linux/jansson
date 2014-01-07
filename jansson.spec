#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	C library for encoding, decoding and manipulating JSON data
Name:		jansson
Version:	2.5
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://www.digip.org/jansson/releases/%{name}-%{version}.tar.gz
# Source0-md5:	46ac93bec48aacf207b67b51c8fbf7f1
URL:		http://www.digip.org/jansson/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_apidocs:BuildRequires:sphinx-pdg}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jansson is a C library for encoding, decoding and manipulating JSON
data. It features:

- Simple and intuitive API and data model
- Comprehensive documentation
- No dependencies on other libraries
- Full Unicode support (UTF-8)
- Extensive test suite

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API and internal documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{_libdir}/lib%{name}.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README.rst
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so
%{_includedir}/%{name}*.h
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib%{name}.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html
%endif
