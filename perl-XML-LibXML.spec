#
# Conditional build:
%bcond_with	tests	# perform "make test"
#
# TODO:
# - add pod files to spec
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	LibXML
Summary:	XML::LibXML - Interface to the gnome libxml2 library
Summary(pl):	XML::LibXML - Interfejs do biblioteki libxml2 z gnome
Name:		perl-%{pdir}-%{pnam}
Version:	1.56
Release:	1
# same as perl
License:	GPL or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/authors/id/P/PH/PHISH/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	e22a4d79e6afdc8965518bf8a3abb492
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-extern.patch
BuildRequires:	gdome2-devel >= 0.7.3
BuildRequires:	libxml2-devel >= 2.5.10
BuildRequires:	perl-XML-LibXML-Common
BuildRequires:	perl-XML-NamespaceSupport >= 1.07
BuildRequires:	perl-XML-SAX >= 0.11
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	libxml2 >= 2.5.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements much of the DOM Level 2 API as an interface to
the GNOME libxml2 library. This makes it a fast and highly capable
validating XML parser library, as well as a high performance DOM.

%description -l pl
Ten modu³ to implementacja wiêkszo¶ci API DOM Level 2 jako interfejsu
do biblioteki GNOME libxml2. Daje to szybki i o du¿ych mo¿liwo¶ciach
parser sprawdzaj±cy poprawno¶æ XML, a tak¿e wysoko wydajny DOM.

%package SAX
Summary:	XML::LibXML::SAX Perl module - XML::LibXML direct SAX parser
Summary(pl):	Modu³ Perla XML::LibXML::SAX - bezpo¶redni parser SAX z XML::LibXML
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}

%description SAX
This class allows you to generate SAX2 events using LibXML. Note that
this is not a stream based parser, instead it parses documents into a
DOM and traverses the DOM tree. The reason being that libxml2's stream
based parsing is extremely primitive, and would require an extreme
amount of work to allow SAX2 parsing in a stream manner.

%description SAX -l pl
Ta klasa pozwala generowaæ zdarzenia SAX2 przy u¿yciu LibXML2. To nie
jest parser bazuj±cy na strumieniach - przetwarza dokumenty na DOM i
nastêpnie wêdruje po drzewie DOM. Wynika to z faktu, ¿e w libxml2
parsowanie oparte na strumieniach jest bardzo prymitywne i wymaga³oby
wiele pracy, aby umo¿liwiæ strumieniowe parsowanie SAX2.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	OPTIMIZE="%{rpmcflags}"

# dtd test fails for unknown reason
%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install example/{*.pl,*.xml,*.dtd,*.xhtml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex
install example/complex/{*.xml,*.dtd} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd
install example/complex/dtd/*.dtd $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/complex/dtd

%clean
rm -rf $RPM_BUILD_ROOT

%post SAX
umask 022
%{__perl} -MXML::SAX -e "XML::SAX->add_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"

%preun SAX
umask 022
%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/XML/LibXML.pm
%{perl_vendorarch}/XML/LibXML/[!S]*.pm
%{perl_vendorarch}/auto/XML/LibXML/LibXML.bs
%attr(755,root,root) %{perl_vendorarch}/auto/XML/LibXML/LibXML.so
%{_mandir}/man3/XML::LibXML.3pm*
%{_mandir}/man3/XML::LibXML::[!S]*
%dir %{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/x*.pl
%{_examplesdir}/%{name}-%{version}/[!x]*

%files SAX
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/XML/LibXML/SAX
%{perl_vendorarch}/XML/LibXML/SAX.pm
%{perl_vendorarch}/XML/LibXML/SAX/*.pm
%{_mandir}/man3/XML::LibXML::SAX.3pm*
%{_mandir}/man3/XML::LibXML::SAX::*
