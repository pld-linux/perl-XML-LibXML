#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	XML
%define		pnam	LibXML
Summary:	XML::LibXML - interface to the GNOME libxml2 library
Summary(pl.UTF-8):	XML::LibXML - interfejs do biblioteki libxml2 z GNOME
Name:		perl-XML-LibXML
Version:	1.65
Release:	2
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/XML/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	7871c21078f706690cda9ca68d4ddac6
URL:		http://search.cpan.org/dist/XML-LibXML/
BuildRequires:	gdome2-devel >= 0.7.3
BuildRequires:	libxml2-devel >= 2.5.10
BuildRequires:	perl-XML-LibXML-Common
BuildRequires:	perl-XML-NamespaceSupport >= 1.07
BuildRequires:	perl-XML-SAX >= 0.11
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	libxml2 >= 2.5.10
Provides:	perl-XML-LibXML-XPathContext = %{version}
Obsoletes:	perl-XML-LibXML-XPathContext <= 0:0.07
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module implements much of the DOM Level 2 API as an interface to
the GNOME libxml2 library. This makes it a fast and highly capable
validating XML parser library, as well as a high performance DOM.

%description -l pl.UTF-8
Ten moduł to implementacja większości API DOM Level 2 jako interfejsu
do biblioteki GNOME libxml2. Daje to szybki i o dużych możliwościach
parser sprawdzający poprawność XML-a, a także wysoko wydajny DOM.

%package SAX
Summary:	XML::LibXML::SAX Perl module - XML::LibXML direct SAX parser
Summary(pl.UTF-8):	Moduł Perla XML::LibXML::SAX - bezpośredni parser SAX z XML::LibXML
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description SAX
This class allows you to generate SAX2 events using LibXML. Note that
this is not a stream based parser, instead it parses documents into a
DOM and traverses the DOM tree. The reason being that libxml2's stream
based parsing is extremely primitive, and would require an extreme
amount of work to allow SAX2 parsing in a stream manner.

%description SAX -l pl.UTF-8
Ta klasa pozwala generować zdarzenia SAX2 przy użyciu LibXML2. To nie
jest parser bazujący na strumieniach - przetwarza dokumenty na DOM i
następnie wędruje po drzewie DOM. Wynika to z faktu, że w libxml2
parsowanie oparte na strumieniach jest bardzo prymitywne i wymagałoby
wiele pracy, aby umożliwić strumieniowe parsowanie SAX2.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
SKIP_SAX_INSTALL=true;
export SKIP_SAX_INSTALL

%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

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
if [ "$1" = "0" ]; then
	umask 022
	%{__perl} -MXML::SAX -e "XML::SAX->remove_parser(q(XML::LibXML::SAX::Parser))->save_parsers()"
fi

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorarch}/XML/LibXML.pm
%{perl_vendorarch}/XML/LibXML/[!S]*.pm
%{perl_vendorarch}/auto/XML/LibXML/LibXML.bs
%attr(755,root,root) %{perl_vendorarch}/auto/XML/LibXML/LibXML.so
%{_mandir}/man3/XML::LibXML.3pm*
%{_mandir}/man3/XML::LibXML::[!S]*
%{_mandir}/man3/XML::LibXML::S[!A]*
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
