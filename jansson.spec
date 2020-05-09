#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	C library for encoding, decoding and manipulating JSON data
Summary(pl.UTF-8):	Biblioteka C do kodowania, dekodowania i obróbki danych JSON
Name:		jansson
Version:	2.13
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://digip.org/jansson/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	64fd100f215c502607a4b0ed531ecb5c
URL:		http://digip.org/jansson/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
BuildRequires:	libtool
%{?with_apidocs:BuildRequires:	sphinx-pdg}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jansson is a C library for encoding, decoding and manipulating JSON
data. It features:
- Simple and intuitive API and data model
- Comprehensive documentation
- No dependencies on other libraries
- Full Unicode support (UTF-8)
- Extensive test suite

%description -l pl.UTF-8
Jansson to biblioteka C do kodowania, dekodowania oraz obróbki danych
JSON. Cechują ją:
- proste i intuicyjne API oraz model danych
- wyczerpująca dokumentacja
- brak zależności od innych bibliotek
- pełna obsługa Unicode (UTF-8)
- obszerny zestaw testów

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for %{name} library.

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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libjansson.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README.rst
%attr(755,root,root) %{_libdir}/libjansson.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjansson.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjansson.so
%{_includedir}/jansson*.h
%{_pkgconfigdir}/jansson.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjansson.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html
%endif
